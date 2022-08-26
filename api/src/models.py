from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False )
    email = db.Column(db.String(100), unique=True, nullable=False )
    password = db.Column(db.String(100), nullable=False)
    characters = db.relationship('Character', backref='user', lazy=True)
    planet = db.relationship('Planet', backref='user', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.username


    def serialize(self):
        return{
            "id" : self.id,
            "username": self.username,
            "email" : self.email
        }
    
    def serialize_with_favorites(self):
        return{
            "id" : self.id,
            "username": self.username,
            "characters": self.get_favorites_characters(),
            "planets": self.get_favorites_planet()
        }

    def get_favorites_characters(self):
        return list(map(lambda character: character.serialize(), self.characters))

    def get_favorites_planets(self):
        return list(map(lambda planet: planet.serialize(), self.planets))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Character(db.Model):
    __tablename__ = 'characters'
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Character %r>' % self.name
    
    def serialize(self):
        return{
            "id" : self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description" : self.description
        }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Planet(db.Model):
    __tablename__ = 'planets'
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def serialize(self):
        return{
            "id" : self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description" : self.description
        }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()