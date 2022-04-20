import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, StringField, BooleanField, IntegerField, FileField, SelectField, DateField
from wtforms.validators import DataRequired, InputRequired


class AddDeliveryForm(FlaskForm):
    method = SelectField('Способ оплаты', choices=['Наличными', 'Картой'])
    status = StringField('Статус заказа', default='В пути')

    submit = SubmitField('Оформить заказ')
