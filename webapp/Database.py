import datetime
import re

import pymysql
from pymysql import IntegrityError


def remove_articles(text):
    return re.sub('(a|an|one|un|une|um|uma)\s+', '', text)


class Database:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.con = None
        self.cur = None

    def open(self):
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db,
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        return self

    def close(self):
        self.cur.close()
        self.con.close()

    def list_recipes(self):
        self.cur.execute("SELECT id, name, notes FROM recipes")
        result = self.cur.fetchall()
        return result

    def list_recipes_ordered(self):
        self.cur.execute("SELECT id, name FROM recipes ORDER BY name")
        result = self.cur.fetchall()
        return result

    def recipes_count(self):
        self.cur.execute("SELECT COUNT(*) FROM recipes")
        result = self.cur.fetchone()['COUNT(*)']
        return result

    def recipe_name(self, recipe_id):
        sql = "SELECT name FROM recipes WHERE id = %s"
        self.cur.execute(sql, recipe_id)
        result = self.cur.fetchone()['name']
        return result

    def recipe_ingredients(self, recipe_id):
        sql = "SELECT id, name, quantity " \
              "FROM recipes_ingredient_rel " \
              "INNER JOIN ingredients ON ingredient_id = id " \
              "WHERE recipe_id = %s"
        self.cur.execute(sql, recipe_id)
        result = self.cur.fetchall()
        return result

    def recipe_ingredients_rel(self):
        self.cur.execute("SELECT id, recipe_id, name, quantity "
                         "FROM recipes_ingredient_rel "
                         "INNER JOIN ingredients ON ingredient_id = id "
                         "ORDER BY recipe_id")
        result = self.cur.fetchall()
        return result

    def ingredients_count(self):
        self.cur.execute("SELECT COUNT(*) FROM ingredients")
        result = self.cur.fetchone()['COUNT(*)']
        return result

    def cocktails_per_day(self):
        self.cur.execute("SELECT COUNT(DISTINCT id) as total, DATE(made_at) as made_at "
                         "FROM history "
                         "GROUP BY DATE(made_at)")
        result = self.cur.fetchall()
        date_list = [(datetime.date.today() - datetime.timedelta(days=x)).strftime("%a %d/%m") for x in
                     reversed(range(10))]
        daily_count = dict.fromkeys(date_list, 0)
        for row in result:
            daily_count[row["made_at"].strftime("%a %d/%m")] = row["total"]
        return list(daily_count.values()), list(daily_count.keys())

    def top_cocktails(self):
        self.cur.execute("SELECT name, COUNT(h.id) as total "
                         "FROM history h "
                         "INNER JOIN recipes ON h.recipe_id = recipes.id "
                         "GROUP BY recipe_id ORDER BY total DESC")
        result = self.cur.fetchall()
        return [row["name"] for row in result], [row["total"] for row in result]

    def glass(self):
        self.cur.execute("SELECT actual_volume, capacity FROM glass WHERE id=1")
        result = self.cur.fetchone()
        return result

    def bottles(self):
        self.cur.execute("SELECT b.id, b.name, ingredient_id, i.name as contents, actual_volume, capacity, "
                         "(actual_volume/capacity)*100 as percentage, enabled "
                         "FROM bottles b "
                         "INNER JOIN ingredients i ON b.ingredient_id = i.id")
        result = self.cur.fetchall()
        return result

    def bottles_simple(self):
        self.cur.execute("SELECT b.id, b.name, ingredient_id, i.name as contents, actual_volume "
                         "FROM bottles b "
                         "INNER JOIN ingredients i ON b.ingredient_id = i.id "
                         "WHERE enabled = 1")
        result = self.cur.fetchall()
        return result

    def ingredients(self):
        self.cur.execute("SELECT * FROM ingredients ORDER BY name")
        result = self.cur.fetchall()
        return result

    def insert_recipe(self, cocktail_name, cocktail_notes, cocktail_ingredients, cocktail_volumes):
        sql = "INSERT INTO recipes (name, notes) VALUES (%s, %s)"
        self.cur.execute(sql, (cocktail_name, cocktail_notes))
        self.con.commit()
        inserted_id = self.cur.lastrowid
        for ingredient, volume in zip(cocktail_ingredients, cocktail_volumes):
            sql = "INSERT INTO recipes_ingredient_rel (recipe_id, ingredient_id, quantity) VALUES (%s, %s, %s)"
            self.cur.execute(sql, (inserted_id, ingredient, volume))
        self.con.commit()

    def update_glass_settings(self, capacity):
        sql = "UPDATE glass SET capacity = %s WHERE id = 1"
        self.cur.execute(sql, capacity)
        self.con.commit()

    def update_bottle_settings(self, name, contents, capacity, enabled, bottle_id):
        sql = "UPDATE bottles SET name = %s, ingredient_id = %s, capacity = %s, enabled = %s WHERE id = %s"
        self.cur.execute(sql, (name, contents, capacity, enabled, bottle_id))
        self.con.commit()

    def make_cocktail(self, recipe_id):
        sql = "INSERT INTO history (recipe_id, made_at) VALUES (%s, %s)"
        self.cur.execute(sql, (recipe_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.con.commit()

    def history(self):
        self.cur.execute(
            "SELECT name, made_at FROM history h INNER JOIN recipes r ON h.recipe_id = r.id ORDER BY made_at")
        result = self.cur.fetchall()
        return result

    def list_recipes_with_ingredients(self):
        recipes = self.list_recipes()
        recipes_ingredients = self.recipe_ingredients_rel()
        for recipes_ingredient in recipes_ingredients:
            recipe = next(item for item in recipes if item['id'] == recipes_ingredient['recipe_id'])
            if 'ingredients' not in recipe:
                recipe['ingredients'] = []
            recipe['ingredients'].append(recipes_ingredient)
        return recipes

    def recipe_with_ingredients(self, recipe_id):
        recipe = {'name': self.recipe_name(recipe_id), 'ingredients': []}
        recipe_ingredients = self.recipe_ingredients(recipe_id)
        for recipe_ingredient in recipe_ingredients:
            recipe['ingredients'].append(recipe_ingredient)
        return recipe

    def insert_ingredient(self, ingredient_name, ingredient_alcohol):
        sql = "INSERT INTO ingredients (name, alcohol) VALUES (%s, %s)"
        self.cur.execute(sql, (ingredient_name, ingredient_alcohol))
        self.con.commit()

    def update_glass_volume(self, volume):
        sql = "UPDATE glass SET actual_volume = %s WHERE id = 1"
        self.cur.execute(sql, volume)
        self.con.commit()

    def update_bottle_volume(self, bottle_id, volume):
        sql = "UPDATE bottles SET actual_volume = %s WHERE id = %s"
        self.cur.execute(sql, (volume, bottle_id))
        self.con.commit()

    def search(self, recipe_name):
        recipe_name = remove_articles(recipe_name)
        sql = "SELECT DISTINCT id FROM recipes WHERE UPPER(name) LIKE UPPER(%s)"
        self.cur.execute(sql, '%' + recipe_name + '%')
        result = self.cur.fetchone()
        if result:
            result = result['id']
        return result

    def delete_ingredient(self, ingredient_id):
        sql = "DELETE FROM recipes_ingredient_rel WHERE ingredient_id = %s"
        self.cur.execute(sql, ingredient_id)
        sql = "DELETE FROM ingredients WHERE id = %s"
        try:
            ret = self.cur.execute(sql, ingredient_id)
            self.con.commit()
        except IntegrityError:
            return False
        return ret > 0

    def delete_recipe(self, recipe_id):
        sql = "DELETE FROM history WHERE recipe_id = %s"
        self.cur.execute(sql, recipe_id)
        sql = "DELETE FROM recipes_ingredient_rel WHERE recipe_id = %s"
        ret = self.cur.execute(sql, recipe_id)
        if ret > 0:
            sql = "DELETE FROM recipes WHERE id = %s"
            ret = self.cur.execute(sql, recipe_id)
            self.con.commit()
            return ret > 0
        return False
