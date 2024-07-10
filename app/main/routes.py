from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.main.forms import CharacterForm, SpellForm
from app.models import Character, Spell, characters_spells_table
from app.extensions import db
from flask_login import login_required, current_user


main = Blueprint('main', __name__)

# Create your routes here.
@main.route('/')
def homepage():
  return render_template('home.html')

@main.route('/characters')
@login_required
def characters():
  characters = current_user.characters
  return render_template('characters.html', user_characters=characters)

@main.route('/spells')
@login_required
def spells():
  spells = current_user.spells
  return render_template('spells.html', spells=spells)

@main.route('/spells/<spell_id>')
@login_required
def spell_details(spell_id):
  spell = Spell.query.get(spell_id)
  characters = Character.query.join(characters_spells_table).filter(
    characters_spells_table.c.spell_id == spell.id, 
    characters_spells_table.c.character_id.in_(
        db.session.query(Character.id).filter(Character.creator_id == current_user.id)
    )
).all()
  spellcasters_list = [character.name for character in characters]
  return render_template('spell_details.html', spell=spell, spellcasters_list=spellcasters_list)

@main.route('/characters/<character_id>')
@login_required
def character_details(character_id):
  character = Character.query.get(character_id)
  spells = Spell.query.join(characters_spells_table).filter(characters_spells_table.c.character_id == character.id).all()
  return render_template('character_details.html', character=character, spells=spells )

@main.route('/characters/new', methods=['GET', 'POST'])
@login_required
def new_character():
  form = CharacterForm()
  if form.validate_on_submit():
    new_character = Character(
      name=form.name.data,
      level=form.level.data,
      class_=form.class_.data,
      creator_id=current_user.id
    )
    db.session.add(new_character)
    db.session.commit()
    flash('Character created successfully!', 'success')
    return redirect(url_for('main.character_details', character_id=new_character.id))
  return render_template('new_character.html', form=form)

@main.route('/spells/new', methods=['GET', 'POST'])
@login_required
def new_spell():
  form = SpellForm()
  if form.validate_on_submit():
    new_spell = Spell(
      name=form.name.data,
      level=form.level.data,
      school=form.school.data,
      description=form.description.data,
      creator_id=current_user.id
    )
    db.session.add(new_spell)
    db.session.commit()
    flash('Spell created successfully!', 'success')
    return redirect(url_for('main.spell_details', spell_id=new_spell.id))
  return render_template('new_spell.html', form=form)

@main.route('/characters/<character_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_character(character_id):
  character = Character.query.get(character_id)
  form = CharacterForm(obj=character)
  if form.validate_on_submit():
    character.name = form.name.data
    character.level = form.level.data
    character.class_ = form.class_.data
    db.session.commit()
    flash('Character updated successfully!', 'success')
    return redirect(url_for('main.character_details', character_id=character.id))
  return render_template('edit_character.html', form=form)

@main.route('/spells/<spell_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_spell(spell_id):
  spell = Spell.query.get(spell_id)
  form = SpellForm(obj=spell)
  if form.validate_on_submit():
    spell.name = form.name.data
    spell.level = form.level.data
    spell.school = form.school.data
    spell.description = form.description.data
    db.session.commit()
    flash('Spell updated successfully!', 'success')
    return redirect(url_for('main.spell_details', spell_id=spell.id))
  return render_template('edit_spell.html', form=form)

@main.route('/characters/<character_id>/delete', methods=['POST'])
@login_required
def delete_character(character_id):
  character = Character.query.get(character_id)
  db.session.delete(character)
  db.session.commit()
  flash('Character deleted successfully!', 'success')
  return redirect(url_for('main.characters'))

@main.route('/spells/<spell_id>/delete', methods=['POST'])
@login_required
def delete_spell(spell_id):
  spell = Spell.query.get(spell_id)
  db.session.delete(spell)
  db.session.commit()
  flash('Spell deleted successfully!', 'success')
  return redirect(url_for('main.spells'))


@main.route('/spells/<spell_id>/learn', methods=['POST'])
def learn_spell(spell_id):
    character_id = request.form['character_id']
    character = Character.query.get(character_id)
    spell = Spell.query.get(spell_id)

    existing_entry = db.session.query(characters_spells_table).filter_by(
        character_id=character.id, spell_id=spell.id).first()
    if existing_entry is not None:
        flash('Spell already learned!', 'danger')
        return redirect(url_for('main.character_details', character_id=character.id))

    learn = characters_spells_table.insert().values(character_id=character.id, spell_id=spell.id)
    db.session.execute(learn)

    db.session.commit()

    return redirect(url_for('main.character_details', character_id=character.id))