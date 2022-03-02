import requests
from models import Character

BASE_URL = "https://www.swapi.tech/api"

def populate_chars():
    response = requests.get(
        f"{BASE_URL}{'people'}"
    )
    body = response.json()
    all_characters = []
    for result in body['results']:
        response = requests.get(result['url'])
        body = response.json()
        all_characters.append(body)
    return all_characters

print(populate_chars())






























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
    
