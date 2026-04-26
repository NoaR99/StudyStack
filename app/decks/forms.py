from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class DeckForm(FlaskForm):
    title       = StringField('Deck Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    is_public   = BooleanField('Make this deck public', default=True)
    submit      = SubmitField('Create Deck')

class CardForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    answer   = TextAreaField('Answer', validators=[DataRequired()])
    submit   = SubmitField('Add Card')
