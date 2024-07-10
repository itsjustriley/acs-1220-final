# Create your models here.
from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  password = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(50), nullable=False, unique=True)
  username = db.Column(db.String(50), nullable=False, unique=True)
  characters = db.relationship('Character', backref='creator', lazy='dynamic')
  spells = db.relationship('Spell', backref='creator', lazy='dynamic')

class Character(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), nullable=False)
  level = db.Column(db.Integer, nullable=False)
  class_ = db.Column(db.String(50), nullable=False)
  spells = db.relationship('Spell', secondary='characters_spells', backref='characters')
  creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Spell(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), nullable=False)
  level = db.Column(db.Integer, nullable=False)
  school = db.Column(db.String(50), nullable=False)
  description = db.Column(db.String(500), nullable=False)
  creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))


users_characters_table = db.Table('users_characters',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('character_id', db.Integer, db.ForeignKey('character.id')),
  db.PrimaryKeyConstraint('user_id', 'character_id')
)

users_spells_table = db.Table('users_spells', 
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('spell_id', db.Integer, db.ForeignKey('spell.id')),
  db.PrimaryKeyConstraint('user_id', 'spell_id')
)

characters_spells_table = db.Table('characters_spells',
  db.Column('character_id', db.Integer, db.ForeignKey('character.id')),
  db.Column('spell_id', db.Integer, db.ForeignKey('spell.id')),
  db.Column('prepared', db.Boolean, nullable=False, default=False),
  db.PrimaryKeyConstraint('character_id', 'spell_id')
)
