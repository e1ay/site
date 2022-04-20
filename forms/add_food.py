from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, StringField, BooleanField, IntegerField, FileField, SelectField
from wtforms.validators import DataRequired, InputRequired


class AddFoodForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    desc = StringField('Описание', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    file = FileField('file', validators=[InputRequired()])
    category = SelectField('categody', choices=['Супы', 'Хачапури', 'Холодные закуски', 'Хинкали', 'Шашлык',
                                                'Соус', 'Салаты', 'Горячие блюда', 'Гарнир', 'Десерты',
                                                'Напитки', ])

    submit = SubmitField('Создать')
