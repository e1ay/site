from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class AddVacancyForm(FlaskForm):
    name = StringField('Название вакансии', validators=[DataRequired()])
    requirements = StringField('Требования', validators=[DataRequired()])
    conditions = StringField('Условия', validators=[DataRequired()])
    pay = StringField('Зарплата', validators=[DataRequired()])

    submit = SubmitField('Добавить')
