import requests

class KeggyApi:
    def __init__(self):
        self.drink_endpoint = 'https://www.thecocktaildb.com/api/json/v1/1/random.php'
        self.monster_endpoint = 'https://www.dnd5eapi.co/api/monsters'
        self.magic_item_endpoint = 'https://www.dnd5eapi.co/api/magic-items'
        self.race_endpoint = 'https://www.dnd5eapi.co/api/races'
  
    def get_drink(self):
        r = requests.get(self.drink_endpoint)
        drink = r.json()['drinks'][0]

        ingredients = []
        for key in drink:
            if 'strIngredient' in key and drink[key] != None:
                strMeasure = key.replace('Ingredient', 'Measure')
                if drink[strMeasure] != None:
                    ingredients.append(drink[strMeasure] + drink[key])
                else:
                    ingredients.append(drink[key])
        
        return {
            'name': drink['strDrink'],
            'ingredients': ', '.join(ingredients[:-1]) + ' and ' + ingredients[-1],
            'instructions': drink['strInstructions'],
            'image': drink['strDrinkThumb']
        }

    def get_races(self, race=None):
        if race == None:
            r = requests.get(self.races_endpoint)
            return r.json()
        if race != None:
            r = requests.get(f'{self.races_endpoint}/{race}')
            return r.json()

    def get_monsters(self, monster_name=None, monster_cr=None):
        if monster_name == None and monster_cr == None:
            r = requests.get(self.monster_endpoint)
            return r.json()
        if monster_name == None and monster_cr != None:
            r = requests.get(f'{self.monster_endpoint}?challenge_rating={monster_cr}')
            return r.json()
        if monster_name != None and monster_cr == None:
            m = monster_name.strip().replace(' ', '-').lower()
            r = requests.get(f'{self.monster_endpoint}/{m}')
            return r.json()

    def get_magic_item(self, item):
        i = item.strip().replace(' ', '-').lower()
        r = requests.get(f'{self.magic_item_endpoint}/{i}')
        return r.json()
