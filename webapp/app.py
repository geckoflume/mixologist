import json
from datetime import datetime

from flask import Flask, render_template, request
from flask_socketio import SocketIO

from Arduino import Arduino
from Database import Database
from Pump import init_pumps, Pump

__author__ = "Florian Mornet"
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = __author__
__email__ = "florian.mornet@bordeaux-inp.fr"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True)  # engineio_logger=True
status = {'type': 'error', 'title': 'Error', 'text': 'No hardware detected', 'val': -1}
pumps = [Pump('bottle1'), Pump('bottle2'), Pump('bottle3'), Pump('bottle4')]


@app.context_processor
def inject():
    db = Database()
    recipes_count = db.recipes_count()
    ingredients_count = db.ingredients_count()
    db.close()
    return dict(recipes_count=recipes_count, ingredients_count=ingredients_count)


def prepare_brewing(cocktail, bottles):
    sequence = []

    for ingredient in cocktail["ingredients"]:
        candidate_bottles = [b for b in bottles if b["enabled"]
                             and b["ingredient_id"] == ingredient["id"]
                             and b["actual_volume"] >= ingredient["quantity"]]
        if not candidate_bottles:
            broadcast_status('error', 'Making ' + cocktail["name"],
                             'Cannot make your cocktail. '
                             'Please check that you have enough quantity of ' + ingredient["name"] +
                             ' in your bottles.', 0)
            return None
        else:
            sequence.append(
                {'bottle': candidate_bottles[0]["id"], 'name': ingredient["name"], 'volume': ingredient["quantity"]})
    return sequence


def make_cocktail(cocktail_id):
    db = Database()
    cocktail = db.recipe_with_ingredients(cocktail_id)
    bottles = db.bottles()
    broadcast_status('ready', 'Making ' + cocktail["name"], 'Starting cocktail...', 0)
    sequence = prepare_brewing(cocktail, bottles)
    if sequence:
        success = True
        for idx in range(len(sequence)):
            s = sequence[idx]
            broadcast_status('ready', 'Making ' + cocktail["name"], 'Pouring ' + s["name"], idx / len(sequence) * 100)
            pumps[s["bottle"] - 1].enable()
            arduino = Arduino()
            wait = arduino.wait_for_glass_measure(s["volume"])
            pumps[s["bottle"] - 1].disable()
            arduino.close()
            if not wait:
                success = False
                broadcast_status('error', 'Making ' + cocktail["name"], 'Pouring ' + s["name"] +
                                 ' timed out, please check that the pumps aren\'t '
                                 'clogged and that you have enough ingredient', idx / len(sequence) * 100)
                break
        if success:
            db.make_cocktail(cocktail_id)
            broadcast_status('success', 'Making ' + cocktail["name"],
                             'Cocktail finished at ' + datetime.now().strftime("%H:%M:%S"), 100)
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
        else:
            return return_code(False)
    else:
        db = Database()
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
    db = Database()
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
    db = Database()
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
    db = Database()
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
            arduino = Arduino()
            ret = arduino.tare(result.get('id'))
            arduino.close()
            return return_code(ret)
        else:
            return return_code(False)
    else:
        bottles = db.bottles()
        ingredients = db.ingredients()
        db.close()
        arduino = Arduino()
        load_cells = arduino.get_measure()
        arduino.close()
        update_volumes()
        return render_template('settings.html', bottles=bottles, ingredients=ingredients, load_cells=load_cells)


@app.route('/list_ingredients')
def list_ingredients():
    db = Database()
    ingredients = db.ingredients()
    db.close()
    return render_template('list_ingredients.html', ingredients=ingredients)


@app.route('/list_recipes')
def list_recipes():
    db = Database()
    recipes = db.list_recipes_with_ingredients()
    db.close()
    return render_template('list_recipes.html', recipes=recipes)


@app.route('/history')
def history():
    db = Database()
    cocktail_history = db.history()
    db.close()
    return render_template('history.html', history=cocktail_history)


def update_volumes():
    arduino = Arduino()
    volumes = arduino.get_measure()
    arduino.close()

    db = Database()
    db.update_bottle_volume(1, volumes["b1"])
    db.update_bottle_volume(2, volumes["b2"])
    db.update_bottle_volume(3, volumes["b3"])
    db.update_bottle_volume(4, volumes["b4"])
    db.close()


def broadcast_status(status_type, status_title, status_text, status_val):
    global status
    status = {'type': status_type, 'title': status_title, 'text': status_text, 'val': status_val}
    print('Broadcasting new status: ' + str(status))
    socketio.emit('status', status, broadcast=True)
    return status


def return_code(success):
    if success:
        return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': success}), 400, {'ContentType': 'application/json'}


def startup_check():
    global status

    try:
        db = Database()
        db.close()
    except:
        status = {'type': 'error', 'title': 'Error', 'text': 'Cannot open connection with the database', 'val': -1}

    arduino = Arduino()
    if not arduino.ser.is_open:
        status = {'type': 'error', 'title': 'Error', 'text': 'Cannot open connection with Arduino', 'val': -1}
    arduino.close()

    try:
        init_pumps()
        status = {'type': 'ready', 'title': 'Ready', 'text': 'Ready to make a new drink', 'val': -1}
    except:
        status = {'type': 'error', 'title': 'Error', 'text': 'Cannot init GPIO', 'val': -1}


if __name__ == '__main__':
    startup_check()
    # app.run(debug=True, host='0.0.0.0')
    socketio.run(app, debug=True, host='0.0.0.0', log_output=True)
