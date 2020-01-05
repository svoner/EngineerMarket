from app import db
from app.auth import bp 
from app.models import User
from flask import redirect, url_for, flash, render_template
from app.auth.forms import LoginForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required


@bp.route('/', methods=['POST', 'GET'])
@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(current_user.get_index()))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('错误的用户名或密码')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for(user.get_index()))
    return render_template('auth/login.html', title='用户登录', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    

@bp.route('/reset_password', methods=['POST', 'GET'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('新密码设置完成')
        return redirect(url_for(current_user.get_index()))
    return render_template(
        'auth/reset_password.html',
        title='Reset Password', form=form)
