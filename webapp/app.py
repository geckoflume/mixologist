from flask import Flask, render_template, request
from flask_socketio import SocketIO

from Database import Database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, logger=True, engineio_logger=True)
socketio = SocketIO(app, logger=True)
status = {'type': 'error', 'title': 'Error', 'text': 'No hardware detected', 'val': -1}


@app.context_processor
def inject():
    db = Database()
    recipes_count = db.recipes_count()
    ingredients_count = db.ingredients_count()
    return dict(recipes_count=recipes_count, ingredients_count=ingredients_count)


# TODO: check POST form attributes before inserting

@app.route('/', methods=['GET', 'POST'])
def index():
    db = Database()
    if request.method == 'POST':
        result = request.form
        cocktail_id = result.get('cocktail')
        db.make_cocktail(cocktail_id)
        cocktail_name = db.recipe_name(cocktail_id)
        broadcast_status('ready', 'Making ' + cocktail_name, 'Starting cocktail...', 0)

    recipes = db.list_recipes_with_ingredients()
    recipes = sorted(recipes, key=lambda k: k['name'].lower())  # to sort by name
    count_days, date_labels = db.cocktails_per_day()
    top_labels, count_top = db.top_cocktails()
    top_css_classes = ['text-primary', 'text-success', 'text-info', 'text-warning', 'text-danger', 'text-light']
    bottles = db.bottles()
    bottles_simple = db.bottles_simple()
    return render_template('index.html', recipes=recipes, day_values=count_days, date_labels=date_labels,
                           top_labels=top_labels, top_values=count_top, top_zip=zip(top_labels, top_css_classes),
                           bottles=bottles, bottles_simple=bottles_simple, status=status)


@app.route('/new_recipe', methods=['GET', 'POST'])
def new_recipe():
    db = Database()
    if request.method == 'POST':
        result = request.form
        cocktail_name = result.get('name')
        cocktail_notes = result.get('notes') if result.get('notes') else None
        cocktail_ingredients = result.getlist('ingredients[]')
        cocktail_volumes = result.getlist('volumes[]')
        db.insert_recipe(cocktail_name, cocktail_notes, cocktail_ingredients, cocktail_volumes)
        socketio.emit('recipes_count', db.recipes_count(), broadcast=True)

    ingredients = db.ingredients()
    return render_template('new_recipe.html', ingredients=ingredients)


@app.route('/new_ingredient', methods=['GET', 'POST'])
def new_ingredient():
    db = Database()
    if request.method == 'POST':
        result = request.form
        ingredient_name = result.get('name')
        ingredient_alcohol = '1' if result.get('alcohol') == 'on' else '0'
        db.insert_ingredient(ingredient_name, ingredient_alcohol)
        socketio.emit('ingredients_count', db.ingredients_count(), broadcast=True)

    return render_template('new_ingredient.html')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    db = Database()
    if request.method == 'POST':
        result = request.form
        name = result.get('name')
        contents = result.get('contents')
        capacity = result.get('capacity')
        bottle_id = result.get('id')
        enabled = '1' if result.get('enabled') == 'on' else '0'
        db.update_bottle_settings(name, contents, capacity, enabled, bottle_id)

    bottles = db.bottles()
    ingredients = db.ingredients()
    return render_template('settings.html', bottles=bottles, ingredients=ingredients)


@app.route('/list_ingredients')
def list_ingredients():
    db = Database()
    ingredients = db.ingredients()
    return render_template('list_ingredients.html', ingredients=ingredients)


@app.route('/list_recipes')
def list_recipes():
    db = Database()
    recipes = db.list_recipes_with_ingredients()
    return render_template('list_recipes.html', recipes=recipes)


@app.route('/history')
def history():
    db = Database()
    cocktail_history = db.history()
    return render_template('history.html', history=cocktail_history)


def broadcast_status(status_type, status_title, status_text, status_val):
    global status
    status = {'type': status_type, 'title': status_title, 'text': status_text, 'val': status_val}
    print('Broadcasting new status: ' + str(status))
    socketio.emit('status', status, broadcast=True)
    return status


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    socketio.run(app, debug=True, host='0.0.0.0', log_output=True)
