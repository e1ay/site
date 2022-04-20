from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, StringField, BooleanField, IntegerField, FileField, SelectField, DateField
from wtforms.validators import DataRequired, InputRequired


class AddDeskForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    places = SelectField('Мест', choices=['1', '2', '3', '4', '5'])
    hours = SelectField('Час', choices=['09', '10', '11', '12', '13', '14', '15', '16',
                                        '17', '18'])
    minut = SelectField('Минута', choices=['00', '30'])
    date = DateField('Дата')

    submit = SubmitField('Забронировать')
