from forms.loginform import LoginForm
from data.users import User
from data.translation import TranslationDB
from forms.user import RegisterForm
from data import db_session
from translator import Translator

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
translator = Translator()
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"


def main():
    db_session.global_init("db/db.db")
    db_sess = db_session.create_session()
    app.run(port=80, host="127.0.0.1")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqistr():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/", methods=['post', 'get'])
def translator_page():
    db_sess = db_session.create_session()
    translated = ""
    original = ""
    from_language = "English"
    to_language = "Russian"
    translations = list()
    # translate = Translation()
    # translate.user_id = 1
    # translate.id = 2
    # translate.queue = 1
    # translate.from_language = "ru"
    # translate.to_language = "en"
    # translate.original_text = "привет"
    # translate.translated_text = "hello"
    # db_sess = db_session.create_session()
    # db_sess.add(translate)
    # db_sess.commit()
    if request.method == 'POST':
        if "input_submit" in request.form:
            original = request.form.get("text_to_translate")
            from_language = request.form.get("language_from")
            to_language = request.form.get("language_to")
            if original:
                translated = translator.translate(from_language, to_language, original)
            if current_user.is_authenticated and original:
                if not db_sess.query(TranslationDB).filter(TranslationDB.user_id == current_user.id).filter(
                        TranslationDB.original_text == original).all():
                    new_translate = TranslationDB()
                    new_translate.user_id = current_user.id
                    new_translate.queue = 0
                    new_translate.from_language = from_language
                    new_translate.to_language = to_language
                    new_translate.original_text = original
                    new_translate.translated_text = translated
                    db_sess.add(new_translate)
                    db_sess.commit()
                    translations_from_bd = db_sess.query(TranslationDB).filter(
                        TranslationDB.user_id == current_user.id).all()
                    for translation in translations_from_bd:
                        translation.queue += 1
                        db_sess.commit()
                        if translation.queue > 5:
                            db_sess.delete(translation)
                            db_sess.commit()

    if current_user.is_authenticated:
        translations_from_bd = db_sess.query(TranslationDB).filter(
            TranslationDB.user_id == current_user.id).order_by(
            TranslationDB.queue).all()
        for t in translations_from_bd:
            translations.append((t.from_language, t.original_text))

    if "1_input" in request.form:
        translation = db_sess.query(TranslationDB).filter(TranslationDB.queue == 1).filter(
            TranslationDB.user_id == current_user.id).one()
        translated = translation.translated_text
        original = translation.original_text
        from_language = translation.from_language
        to_language = translation.to_language
    elif "2_input" in request.form:
        translation = db_sess.query(TranslationDB).filter(TranslationDB.queue == 2).filter(
            TranslationDB.user_id == current_user.id).one()
        translated = translation.translated_text
        original = translation.original_text
        from_language = translation.from_language
        to_language = translation.to_language
    elif "3_input" in request.form:
        translation = db_sess.query(TranslationDB).filter(TranslationDB.queue == 3).filter(
            TranslationDB.user_id == current_user.id).one()
        translated = translation.translated_text
        original = translation.original_text
        from_language = translation.from_language
        to_language = translation.to_language
    elif "4_input" in request.form:
        translation = db_sess.query(TranslationDB).filter(TranslationDB.queue == 4).filter(
            TranslationDB.user_id == current_user.id).one()
        translated = translation.translated_text
        original = translation.original_text
        from_language = translation.from_language
        to_language = translation.to_language
    elif "5_input" in request.form:
        translation = db_sess.query(TranslationDB).filter(TranslationDB.queue == 5).filter(
            TranslationDB.user_id == current_user.id).one()
        translated = translation.translated_text
        original = translation.original_text
        from_language = translation.from_language
        to_language = translation.to_language

    return render_template("translator.html", translated=translated, original=original, translations=translations,
                           from_language=from_language, to_language=to_language, title="Translator")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
