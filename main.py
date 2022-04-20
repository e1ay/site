import datetime
import os
import secrets

from flask import Flask, render_template, redirect, request, flash, url_for, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from utils import *
from data import db_session
from data.delivery import Delivery
from data.desk import Desk
from data.food import Foods
from data.orders import Order
from data.users import User
from data.vacancy import Vacancy
from forms.add_delivery import AddDeliveryForm
from forms.add_desk import AddDeskForm
from forms.add_food import AddFoodForm
from forms.add_vacancy import AddVacancyForm
from forms.login_form import LoginForm
from forms.register_form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ajajajajajaj'
app.config['UPLOAD_FOLDER'] = 'static/img/food_img'

login_manager = LoginManager()
login_manager.init_app(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/addfood', methods=['GET', 'POST'])
def addfood():
    add_form = AddFoodForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        foods = Foods(
            name=add_form.name.data,
            desc=add_form.desc.data,
            price=add_form.price.data,
            pic=filename,
            category=add_form.category.data
        )
        db_sess.add(foods)
        db_sess.commit()
        return redirect('/')
    return render_template('addfood.html', title='Adding a food', form=add_form)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/addvacancy', methods=['GET', 'POST'])
@login_required
def addvacancy():
    add_form = AddVacancyForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Vacancy(
            name=add_form.name.data,
            requirements=add_form.requirements.data,
            conditions=add_form.conditions.data,
            pay=add_form.pay.data
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/vacancy')
    return render_template('addvacancy.html', title='Adding a vacancy', form=add_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            patronymic=form.patronymic.data,
            telephone=form.telephone.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/register/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    form = RegisterForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        jobs = db_sess.query(User).filter(current_user.get_id() == f'{str(id)}').first()
        if jobs:
            form.name.data = jobs.name
            form.surname.data = jobs.surname
            form.email.data = jobs.email
            form.patronymic.data = jobs.patronymic
            form.telephone.data = jobs.telephone
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(User).filter(current_user.get_id() == f'{str(id)}').first()
        if jobs:
            jobs.name = form.name.data
            jobs.surname = form.surname.data
            jobs.email = form.email.data
            jobs.patronymic = form.patronymic.data
            jobs.telephone = form.telephone.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('register.html', title='Edit a profile', form=form)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    foods = db_sess.query(Foods).all()
    title = 'Главная'
    return render_template('index.html', foods=foods, title=title)


@app.route('/delivery')
def page():
    title = 'Доставка'
    return render_template('delivery.html', active_d='active', title=title)


@app.route('/order')
def order():
    title = 'Оплата'
    return render_template('order.html', active_o='active', title=title)


@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    title = 'Бронь стола'
    form = AddDeskForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        desks = db_sess.query(Desk).all()
        jobs = Desk(
            name=form.name.data,
            surname=form.surname.data,
            date=form.date.data,
            time=form.hours.data + ':' + form.minut.data,
            places=form.places.data,
            user_id=current_user.get_id()
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    db_sess = db_session.create_session()
    desks = db_sess.query(Desk).all()
    return render_template('booking.html', active_b='active', title=title, form=form, desks=desks)


@app.route('/desks_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def desks_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Desk).filter(Desk.id == id,
                                      current_user.get_id() == '1' or current_user.get_id() == f'{str(id)}').first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/booking')


@app.route('/support')
def support():
    title = 'Поддержка'
    return render_template('help.html', title=title)


@app.route('/card/<int:id>')
def card(id):
    db_sess = db_session.create_session()
    card = db_sess.query(Foods).filter(Foods.id == id).first()
    need = 3000 - int(card.price)
    cir = card.price - card.price // 3
    return render_template('card.html', card=card, need=need, cir=cir)


@app.route('/vacancy')
def vacancy():
    title = 'Вакансии'
    db_sess = db_session.create_session()
    vacancy = db_sess.query(Vacancy).all()
    return render_template('vacancy.html', jobs=vacancy, title=title)


@app.route('/cart-order', methods=['GET', 'POST'])
def cart_order():
    db_sess = db_session.create_session()
    order = db_sess.query(Order).filter(Order.user_id == current_user.get_id()).all()
    all_price = 0
    for i in order:
        all_price += i.price
    divi = 0
    if all_price >= 3000:
        divi = 0
    else:
        divi = 500

    total = all_price + divi

    form = AddDeliveryForm()
    db_sess = db_session.create_session()
    deliverys = db_sess.query(Delivery).all()

    if form.validate_on_submit():
        jobs = Delivery(
            method=form.method.data,
            get_date=str(datetime.date.today()),
            give_date=str(datetime.date.today() + datetime.timedelta(days=1)),
            status=form.status.data,
            user_id=current_user.get_id()
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    else:
        print(form.errors)

        return render_template('cart-order.html', order=order, all_price=all_price, divi=divi, total=total, form=form)


@app.route('/cart-delete/<int:id>')
def cart_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Order).filter(Order.id == id).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/cart-order')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    title = 'Профиль'
    db_sess = db_session.create_session()
    jobs = db_sess.query(Delivery).filter(Delivery.user_id == current_user.get_id()).all()
    order = db_sess.query(Order).filter(Order.user_id == current_user.get_id()).all()
    return render_template('profile.html', title=title, jobs=jobs, order=order)


@app.route('/to-cart/<int:id>', methods=['GET', 'POST'])
def to_cart(id):
    db_sess = db_session.create_session()
    foods = db_sess.query(Foods).filter(Foods.id == id).first()
    order = Order(
        name=foods.name,
        desc=foods.desc,
        price=foods.price,
        category=foods.category,
        pic=foods.pic,
        user_id=current_user.get_id()
    )
    db_sess.add(order)
    db_sess.commit()
    return redirect('/')


def main():
    db_session.global_init("db/database.sqlite")

    app.run()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(401)
def page_not_found(e):
    return render_template('401.html'), 401


if __name__ == '__main__':
    main()
