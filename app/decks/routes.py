from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.decks.forms import DeckForm, CardForm
from app.models import Deck, Card, Tag
from app import db

decks_bp = Blueprint('decks', __name__)


@decks_bp.route('/decks')
@login_required
def deck_list():
    decks = Deck.query.filter_by(user_id=current_user.id).order_by(Deck.created_at.desc()).all()
    return render_template('decks/index.html', decks=decks)

@decks_bp.route('/decks/create', methods=['GET', 'POST'])
@login_required
def deck_create():
    form = DeckForm()
    if form.validate_on_submit():
        deck = Deck(
            title=form.title.data,
            description=form.description.data,
            is_public=form.is_public.data,
            owner=current_user
        )
        deck.tags = process_tags(form.tags.data)
        db.session.add(deck)
        db.session.commit()
        flash('Deck created successfully!', 'success')
        return redirect(url_for('decks.deck_detail', deck_id=deck.id))
    return render_template('decks/create.html', form=form)

@decks_bp.route('/decks/<int:deck_id>')
def deck_detail(deck_id):
    deck = db.get_or_404(Deck, deck_id)
    if not deck.is_public and (not current_user.is_authenticated or deck.owner !=current_user):
        abort(403)
    return render_template('decks/detail.html', deck=deck)

@decks_bp.route('/decks/<int:deck_id>/matching_game')
def matching_game(deck_id):
    deck = db.get_or_404(Deck, deck_id)
    if not deck.is_public and (not current_user.is_authenticated or deck.owner !=current_user):
        abort(403)
    return render_template('decks/matching.html', deck=deck)

@decks_bp.route('/decks/<int:deck_id>/cards/new', methods=['GET', 'POST'])
@login_required
def card_create(deck_id):
    deck = db.get_or_404(Deck, deck_id)
    if deck.owner != current_user:
        abort(403)
    form = CardForm()
    if form.validate_on_submit():
        card = Card(
            question=form.question.data,
            answer=form.answer.data,
            deck_id=deck.id
        )
        db.session.add(card)
        db.session.commit()
        flash('Card added!', 'success')
        return redirect(url_for('decks.deck_detail', deck_id=deck.id))
    return render_template('decks/new_card.html', form=form, deck=deck)

def process_tags(tag_string):
    """
    turn a comma-separated tag string into a list of Tag objects.
    existing tags are reused; new ones are created

    'Python, flask, AI -> [<Tag python>, <Tag flask>, <Tag ai>]'
    """
    if not tag_string:
        return []

    tag_objects = []
    for raw in tag_string.split(','):
        name = raw.strip().lower()
        if not name:
            continue
        tag = Tag.query.filter_by(name=name).first()
        if tag in None:
            tag = Tag(name=name)
            db.session.add(tag)
        tag_objects.append(tag)

    return tag_objects