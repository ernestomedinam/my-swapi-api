from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created = db.Column(db.DateTime(timezone=True), default=db.func.now())
    updated = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now())


class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Item(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    nature = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': nature
    }

    def __repr__(self) -> str:
        return f"{self.id}: {self.name}, {self.nature}"

    def __init__(self, *args, **kwargs): # keyword arguments
        """
            kwargs = {
                "name": "Luke",
                "eye_color": "brown",
                ...
            }
        """
        for (key, value) in kwargs.items(): #
            if key in ('created', 'updated'): continue
            if hasattr(self, key): #
                attribute_type = getattr(self.__class__, key).type
                try:
                    attribute_type.python_type(value)
                    setattr(self, key, value) #

                except Exception as error:
                    print("ignoring key ", key, " with ", value, " for ", attribute_type.python_type, " because ", error.args)

    @classmethod
    def create(cls, data):
        # crear la instancia
        instance = cls(**data)
        if (not isinstance(instance, cls)): 
            print("FALLA EL CONSTRUCTOR")
            return None
        # guardar en bdd
        db.session.add(instance)
        try:
            db.session.commit()
            print(f"created: {instance.name}")
            return instance
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)

class Character(Item):
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    mass = db.Column(db.Numeric(precision=6, scale=2))
    height = db.Column(db.Numeric(precision=6, scale=2))
    skin_color = db.Column(db.String(80))
    eye_color = db.Column(db.String(80))
    hair_color = db.Column(db.String(80))

    __mapper_args__ = {
        'polymorphic_identity': 'character'
    }

    def __repr__(self) -> str:
        return f"{self.id}: {self.name}, {self.nature}, {self.eye_color}"

    def serialize(self):
        """
            devuelve un diccionario que represetna al objeto
            para poder convertirlo en json y responder al front end
        """
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color
        }

    def shortalize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": f"http://127.0.0.1:3000/{self.nature}s/{self.id}"
        }

class Planet(Item):
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    terrain = db.Column(db.String())
    climate = db.Column(db.String())
    population = db.Column(db.Numeric(precision=20, scale=0))

    __mapper_args__ = {
        'polymorphic_identity': 'planet'
    }

class Starship(Item):
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'starship'
    }

