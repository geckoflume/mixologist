import configparser
import json
import logging
import threading
from datetime import datetime

import requests
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room
from pymysql import DatabaseError
from serial import SerialException

from Arduino import Arduino
from Database import Database
from Pump import init_pumps, Pump
from WS2812 import WS2812

__author__ = "Florian Mornet"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = __author__
__email__ = "florian.mornet@bordeaux-inp.fr"

status = {'type': 'error', 'title': 'Startup check', 'text': 'No hardware detected', 'val': -1}
config = configparser.ConfigParser()
config.read('config.ini')

# Debug
debug = config.getboolean('Mixologist', 'Debug', fallback=False)
if not debug:
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)


# IFTTT
IFTTT_url = config.get('IFTTT', 'URL', fallback='')

# DB check
db_host = config.get('Database', 'Host', fallback="127.0.0.1")
db_user = config.get('Database', 'User', fallback="root")
db_password = config.get('Database', 'Password', fallback="")
db_db = config.get('Database', 'Db', fallback="mixologist")
try:
    db = Database(db_host, db_user, db_password, db_db)
    db.open()
except DatabaseError:
    status = {'type': 'error', 'title': 'Startup check', 'text': 'Cannot open connection with the database', 'val': -1}

# Arduino check
arduino_port = config.get('Arduino', 'Port', fallback="/dev/ttyACM0")
arduino_baudrate = config.getint('Arduino', 'BaudRate', fallback=57600)
arduino_con_timeout = config.getint('Arduino', 'ConTimeout', fallback=5)
arduino_pump_timeout = config.getint('Arduino', 'PumpTimeout', fallback=60)
try:
    arduino = Arduino(arduino_port, arduino_baudrate, arduino_con_timeout, arduino_pump_timeout)
except SerialException:
    status = {'type': 'error', 'title': 'Startup check', 'text': 'Cannot open connection with Arduino', 'val': -1}

# Pumps GPIO check
try:
    init_pumps()
    status = {'type': 'ready', 'title': 'Ready', 'text': 'Ready to make a new drink', 'val': -1}
except OSError:
    status = {'type': 'error', 'title': 'Startup check', 'text': 'Cannot init GPIO', 'val': -1}

# WS2812 LEDs check
ws2812_port = config.getint('WS2812', 'Bus', fallback=0)
ws2812_dev = config.getint('WS2812', 'Device', fallback=0)
ws2812_led_count = config.getint('WS2812', 'LEDCount', fallback=10)
try:
    ws2812 = WS2812(ws2812_port, ws2812_dev, ws2812_led_count)
    ws2812.reset()
except (OSError, OverflowError):
    status = {'type': 'error', 'title': 'Startup check', 'text': 'Cannot open SPI port for LED status', 'val': -1}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=debug, engineio_logger=debug)

pumps = [Pump('bottle1'), Pump('bottle2'), Pump('bottle3'), Pump('bottle4')]
loadcell_trigger = threading.Event()
cocktail_trigger = threading.Event()
settings_room = []
index_room = []


@app.context_processor
def inject():
    db.open()
    recipes_count = db.recipes_count()
    ingredients_count = db.ingredients_count()
    db.close()
    return dict(recipes_count=recipes_count, ingredients_count=ingredients_count)


def prepare_brewing(cocktail, glass, bottles):
    sequence = []
    target_volume = arduino.json_line['g']

    for ingredient in cocktail["ingredients"]:
        candidate_bottles = [b for b in bottles if b["enabled"]
                             and b["ingredient_id"] == ingredient["id"]
                             and b["actual_volume"] >= ingredient["quantity"]]
        if candidate_bottles:
            sequence.append(
                {'bottle': candidate_bottles[0]["id"], 'name': ingredient["name"], 'volume': ingredient["quantity"]})
            target_volume += ingredient["quantity"]
            if target_volume > glass['capacity']:
                broadcast_status('error', 'Making ' + cocktail["name"],
                                 'Cannot make your cocktail: Your glass would overflow.', 0)
                return None, None

        else:
            broadcast_status('error', 'Making ' + cocktail["name"],
                             'Cannot make your cocktail: '
                             'Please check that you have enough quantity of ' + ingredient["name"] +
                             ' in your bottles.', 0)
            return None, None
    return sequence, target_volume


def make_cocktail(cocktail_id):
    db.open()
    cocktail = db.recipe_with_ingredients(cocktail_id)
    glass = db.glass()
    bottles = db.bottles()
    broadcast_status('ready', 'Making ' + cocktail["name"], 'Starting cocktail...', 0)
    sequence, target_volume = prepare_brewing(cocktail, glass, bottles)
    if sequence:
        success = True
        arduino.target_glass_volume = target_volume
        if not cocktail_trigger.isSet():
            cocktail_trigger.set()
        for idx in range(len(sequence)):
            s = sequence[idx]
            broadcast_status('ready', 'Making ' + cocktail["name"], 'Pouring ' + s["name"])
            pumps[s["bottle"] - 1].enable()
            wait = arduino.wait_for_glass_measure(s["volume"])
            pumps[s["bottle"] - 1].disable()
            if not wait:  # timeout or abort
                success = False
                if arduino.abort:
                    broadcast_status('error', 'Making ' + cocktail["name"], 'Aborted')
                    arduino.abort = False
                else:
                    broadcast_status('error', 'Making ' + cocktail["name"], 'Pouring ' + s["name"] +
                                     ' timed out, please check that the pumps aren\'t '
                                     'clogged and that you have enough ingredient')
                break
        if success:
            db.make_cocktail(cocktail_id)
            broadcast_status('success', 'Making ' + cocktail["name"],
                             'Cocktail finished at ' + datetime.now().strftime("%H:%M:%S"), 100)
        if cocktail_trigger.isSet():
            cocktail_trigger.clear()
    db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    update_volumes()
    if request.method == 'POST':
        result = request.form
        if 'cocktail' in result:
            cocktail_id = result.get('cocktail')
            make_cocktail(cocktail_id)
            return return_code(True)
        elif 'abort' in result:
            broadcast_status('error', '', 'Aborting cocktail...')
            arduino.abort = True
            return return_code(True)
        else:
            return return_code(False)
    else:
        db.open()
        recipes = db.list_recipes_with_ingredients()
        recipes = sorted(recipes, key=lambda k: k['name'].lower())  # to sort by name
        count_days, date_labels = db.cocktails_per_day()
        top_labels, count_top = db.top_cocktails()
        top_css_classes = ['text-primary', 'text-success', 'text-info', 'text-warning', 'text-danger', 'text-light']
        bottles = db.bottles()
        bottles_simple = db.bottles_simple()
        db.close()
        return render_template('index.html', recipes=recipes, day_values=count_days, date_labels=date_labels,
                               top_labels=top_labels, top_values=count_top, top_zip=zip(top_labels, top_css_classes),
                               bottles=bottles, bottles_simple=bottles_simple, status=status)


@app.route('/new_recipe', methods=['GET', 'POST'])
def new_recipe():
    db.open()
    if request.method == 'POST':
        result = request.form
        if 'name' in result and 'ingredients[]' in result and 'volumes[]' in result:
            cocktail_name = result.get('name')
            cocktail_notes = result.get('notes') if result.get('notes') else None
            cocktail_ingredients = result.getlist('ingredients[]')
            cocktail_volumes = result.getlist('volumes[]')
            db.insert_recipe(cocktail_name, cocktail_notes, cocktail_ingredients, cocktail_volumes)
            socketio.emit('recipes_count', db.recipes_count(), broadcast=True)
            db.close()
            return return_code(True)
        else:
            return return_code(False)
    else:
        ingredients = db.ingredients()
        db.close()
        return render_template('new_recipe.html', ingredients=ingredients)


@app.route('/new_ingredient', methods=['GET', 'POST'])
def new_ingredient():
    db.open()
    if request.method == 'POST':
        result = request.form
        if 'name' in result:
            ingredient_name = result.get('name')
            ingredient_alcohol = '1' if result.get('alcohol') == 'on' else '0'
            db.insert_ingredient(ingredient_name, ingredient_alcohol)
            socketio.emit('ingredients_count', db.ingredients_count(), broadcast=True)
            db.close()
            return return_code(True)
        else:
            return return_code(False)
    else:
        return render_template('new_ingredient.html')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    db.open()
    if request.method == 'POST':
        result = request.form
        if 'name' in result and 'contents' in result and 'capacity' in result and 'id' in result:
            print('Applying settings for bottle ' + result.get('id'))
            name = result.get('name')
            contents = result.get('contents')
            capacity = result.get('capacity')
            bottle_id = result.get('id')
            enabled = '1' if result.get('enabled') == 'on' else '0'
            db.update_bottle_settings(name, contents, capacity, enabled, bottle_id)
            db.close()
            return return_code(True)
        elif 'id' in result:
            print('Request tare for load cell ' + result.get('id'))
            ws2812.reset()
            ws2812.enable_pos(result.get('id'), WS2812.ready)
            ret = arduino.tare(result.get('id'))
            ws2812.reset()
            return return_code(ret)
        elif 'capacity' in result:
            print('Applying settings for glass')
            capacity = result.get('capacity')
            db.update_glass_settings(capacity)
            db.close()
            return return_code(True)
        else:
            return return_code(False)
    else:
        glass = db.glass()
        bottles = db.bottles()
        ingredients = db.ingredients()
        db.close()
        update_volumes()
        return render_template('settings.html', glass=glass, bottles=bottles, ingredients=ingredients)


@app.route('/list_ingredients')
def list_ingredients():
    db.open()
    ingredients = db.ingredients()
    db.close()
    return render_template('list_ingredients.html', ingredients=ingredients)


@app.route('/list_recipes')
def list_recipes():
    db.open()
    recipes = db.list_recipes_with_ingredients()
    db.close()
    return render_template('list_recipes.html', recipes=recipes)


@app.route('/history')
def history():
    db.open()
    cocktail_history = db.history()
    db.close()
    return render_template('history.html', history=cocktail_history)


@app.route('/search', methods=['POST'])
def search():
    if 'query' in request.get_json():
        print('New search query: ' + request.get_json()['query'])
        db.open()
        cocktail_id = db.search(request.get_json()['query'])
        db.close()
        if cocktail_id:
            make_cocktail(cocktail_id)
            return return_code(True)
        return return_code(False, 404)
    return return_code(False)


@socketio.on('settings')
def join_settings():
    if request.sid not in settings_room:
        join_room('settings')
        print(request.sid + " joined settings")
        settings_room.append(request.sid)
        if not loadcell_trigger.isSet():
            loadcell_trigger.set()
        print('Users in settings: ' + str(settings_room))
    else:
        print('Error, ' + request.sid + 'already in settings room')


@socketio.on('index')
def join_index():
    if request.sid not in index_room:
        join_room('index')
        print(request.sid + " joined index")
        index_room.append(request.sid)
        if not loadcell_trigger.isSet():
            loadcell_trigger.set()
        print('Users in index: ' + str(index_room))
    else:
        print('Error, ' + request.sid + 'already in index room')


@socketio.on('disconnect')
def test_disconnect():
    if request.sid in settings_room:
        settings_room.remove(request.sid)
        print(request.sid + ' has left the settings')
        if len(settings_room) == 0 and len(index_room) == 0 and loadcell_trigger.isSet():
            loadcell_trigger.clear()
    if request.sid in index_room:
        index_room.remove(request.sid)
        print(request.sid + ' has left index')
        if len(index_room) == 0 and cocktail_trigger.isSet():
            cocktail_trigger.clear()
        if len(index_room) == 0 and len(settings_room) == 0 and loadcell_trigger.isSet():
            loadcell_trigger.clear()


def update_volumes():
    volumes = arduino.poll_once()
    db.open()
    db.update_bottle_volume(1, volumes["b1"])
    db.update_bottle_volume(2, volumes["b2"])
    db.update_bottle_volume(3, volumes["b3"])
    db.update_bottle_volume(4, volumes["b4"])
    db.update_glass_volume(volumes["g"])
    db.close()


def broadcast_status(status_type, status_title, status_text, status_val=None):
    global status
    if status_val is None:
        status_val = status['val']
    status = {'type': status_type, 'title': status_title, 'text': status_text, 'val': status_val}
    print('Broadcasting new status: ' + str(status))
    socketio.emit('status', status, room='index')

    requests.post(IFTTT_url, json={'value1': status_title, 'value2': status_text})
    ws2812.reset()
    if status_val == -1:
        ws2812.enable_all(status_type)
    else:
        ws2812.enable_n(int(status_val), status_type)

    return status


def return_code(success, code=400):
    if success:
        return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': success}), code, {'ContentType': 'application/json'}


if __name__ == '__main__':
    arduino_settings_thread = threading.Thread(name='ArduinoSettingsThread', target=arduino.broadcast_loadcells,
                                               args=(loadcell_trigger, socketio,))
    arduino_cocktail_thread = threading.Thread(name='ArduinoCocktailThread', target=arduino.update_progression,
                                               args=(cocktail_trigger, socketio, ws2812,))
    arduino_settings_thread.start()
    arduino_cocktail_thread.start()
    socketio.run(app, debug=debug, host='0.0.0.0', log_output=debug, ssl_context='adhoc')
