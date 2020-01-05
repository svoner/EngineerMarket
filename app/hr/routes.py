
import os
from app import db
from app.hr import bp
from app.hr.forms import UserEditForm
from app.models import User, Code
from flask import redirect, request, render_template, current_app, flash, url_for
from flask_login import current_user, login_required
from datetime import datetime


@bp.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(
        page, current_app.config['HR_ENGINEERS_PER_PAGE'], False)
    return render_template(
        'hr/index.html', title='人员信息',
        users=users.items, pagination=users)


@bp.route('edit_user', methods=['POST', 'GET'])
@login_required
def edit_user():
    user_id = request.args.get('id', 0, type=int)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        form = UserEditForm()
    else:
        form = UserEditForm(user.username, user.email)
    if form.validate_on_submit():
        if user is None:
            user = User(
                username=form.username.data,
                name=form.name.data,
                role_id=form.role.data,
                state_id=Code.free,
                email=form.email.data,
                phone=form.phone.data,
                gender=form.gender.data,
                is_manager=form.is_manager.data)
            user.set_password('default')
            if form.upload.data:
                upload_file = form.upload.data
                filename = '{}.{}'.format(
                    datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'),
                    upload_file.filename.split('.')[-1])
                upload_file.save(os.path.join(
                    current_app.config['UPLOAD_PATH'], filename))
                user.avatar = filename
            db.session.add(user)
            db.session.commit()
            flash('用户[{}]添加成功'.format(user.name))
        else:
            user.username = form.username.data
            user.name = form.name.data
            user.role_id = form.role.data
            user.email = form.email.data
            user.phone = form.phone.data
            user.gender = form.gender.data
            user.is_manager = form.is_manager.data
            if form.upload.data:
                upload_file = form.upload.data
                filename = '{}.{}'.format(
                    datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'),
                    upload_file.filename.split('.')[-1])
                upload_file.save(os.path.join(
                    current_app.config['UPLOAD_PATH'], filename))
                os.remove(os.path.join(
                    current_app.config['UPLOAD_PATH'], user.avatar))
                user.avatar = filename
            db.session.commit()
            flash('用户[{}]更新成功'.format(user.name))
        return redirect(url_for('hr.index'))
    if user is not None:
        form.username.data = user.username
        form.name.data = user.name
        form.role.data = user.role_id
        form.email.data = user.email
        form.phone.data = user.phone
        form.gender.data = user.gender
        form.is_manager.data = user.is_manager
    return render_template(
        'hr/user_edit.html', form=form, title='用户编辑',
        user=user)


@bp.route('reset_password')
@login_required
def reset_password():
    user_id = request.args.get('id', 0, type=int)
    user = User.query.filter_by(id=user_id).first_or_404()
    if user is not None:
        user.set_password('default')
        db.session.commit()
    flash('密码已重置为 default')
    return redirect(url_for('hr.index'))
