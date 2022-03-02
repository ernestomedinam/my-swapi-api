from models import Character, Item
from flask import current_app as app


@app.cli.command("create-character")
def create_character():
    with app.app_context():
        character = Character.create(
            name="Jose",
            eye_color="blue"
        )
        print(character.serialize())
