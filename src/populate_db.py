from email.policy import default
import click
import requests
from models import Character, Planet, Starship
from flask import current_app as app

BASE_URL = "https://www.swapi.tech/api"


@app.cli.command("populate-db")
@click.argument('amount', type=click.INT, default=1)
def populate_db(amount=1):
    for (swapi_end, resource) in [
        ('/people', 'character'),
        ('/planets', 'planet'),
        ('/starships', 'starship')
    ]:
        populate_items(swapi_end, resource, amount)

def populate_items(swapi_end, resource, amount):
    print(f"starting {resource}s requests")
    response = requests.get(
        f"{BASE_URL}{swapi_end}/?page=1&limit={amount}"
    )
    results = response.json()['results']
    all_items = []
    for result in results:
        response = requests.get(result['url'])
        properties = response.json()['result']['properties']
        all_items.append(properties)
    items = []
    print(f"creating {resource}s instances")
    for item in all_items:
        item_instance = None
        if resource == "character":
            item_instance = Character.create(item)
        elif resource == "planet":
            item_instance = Planet.create(item)
        else:
            item_instance = Starship.create(item)
        if item_instance is None: continue
        items.append(item_instance)
    print(f"created {len(items)} {resource}s")





























    # for character in all_characters:
    #     data = {**character['result']['properties']}
    #     instance = Character(
    #         name=data['name'],
    #         mass=data['mass'],
    #         skin_color=data['skin_color'],
    #         eye_color=data['eye_color']
    #     )
    #     if isinstance(instance, Character):
    #         print(f"created {instance.name} with id:{instance.id}")
    #         continue
    #     else:
    #         print("ay, algo pasó.")
    
