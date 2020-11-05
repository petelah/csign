from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class TodoForm(FlaskForm):
    content = TextAreaField('Add your todo:', validators=[DataRequired()])
    submit = SubmitField('Add')