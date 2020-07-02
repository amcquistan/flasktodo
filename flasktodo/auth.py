
from flask import flash, render_template, url_for, redirect, request, Blueprint

from flask_login import LoginManager, login_user, logout_user, login_required

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flasktodo.models import db, User

login_manager = LoginManager()

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@bp.route('/register')
def show_register():
    return render_template('auth/register.html')


@bp.route('/register', methods=('POST',))
def register():
    username = request.form['username']
    raw_password1 = request.form['password1']
    raw_password2 = request.form['password2']
    
    if not username:
        flash('Username is a required field')
        return redirect(url_for('auth.show_register'))

    if not raw_password1 or not raw_password2:
        flash('Password is a required field')
        return redirect(url_for('auth.show_register'))

    if raw_password1 != raw_password2:
        flash('Passwords do not match')
        return redirect(url_for('auth.show_register'))

    if len(raw_password1) < 8:
        flash('Password must be at least 8 characters')
        return redirect(url_for('auth.show_register'))

    user = User(username=username, password=generate_password_hash(raw_password1))
    db.session.add(user)
    db.session.commit()
    login_user(user)

    return redirect(url_for('todo.index'))


@bp.route('/login')
def show_login():
    return render_template('auth/login.html')


@bp.route('/login', methods=('POST',))
def login():
    username = request.form['username']
    raw_password = request.form['password']
    
    if not username:
        flash('Username is a required field')
        return redirect(url_for('auth.show_login'))

    if not raw_password:
        flash('Password is a required field')
        return redirect(url_for('auth.show_login'))
    
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, raw_password):
        flash('Invalid credentials')
        return redirect(url_for('auth.show_login'))
    
    login_user(user)
    
    return redirect(url_for('todo.index'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
