# Create your forms here.

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from app.models import Character
from flask_login import current_user

class CharacterForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  level = IntegerField('Level', validators=[DataRequired()])
  class_ = StringField('Class', validators=[DataRequired()])
  submit = SubmitField('Submit')

class SpellForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  level = IntegerField('Level', validators=[DataRequired()])
  school = StringField('School', validators=[DataRequired()])
  description = StringField('Description', validators=[DataRequired()])
  submit = SubmitField('Submit')