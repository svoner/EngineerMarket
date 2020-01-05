from app.engineer import bp
from app import db
from app.engineer.forms import LogForm, SkillEditForm
from app.models import Order, User, Log, Product, Skills, Role, Code
from flask import url_for, redirect, render_template, request, current_app, flash
from flask_login import current_user, login_required
from sqlalchemy import func


@bp.route('/index')
@login_required
def index():
    new_orders = Order.query.filter_by(
        engineer=current_user).filter(Order.state_id == Code.wait).all()
    skill_top10 = db.session.query(
        Skills, Skills.user_id, func.sum(Skills.level)).group_by(
            Skills.user_id).order_by(
                func.sum(Skills.level).desc()).limit(10).all()

    order_top10 = db.session.query(
        User, Order, func.count(User.name)).filter(
            User.id == Order.engineer_id).group_by(
                User.name).order_by(
                    func.count(User.name).desc()).limit(10).all()
    return render_template(
        'engineer/index.html', title='主页',
        skill_top10=skill_top10, order_top10=order_top10,
        new_orders=new_orders)


@bp.route('/orders')
@login_required
def orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(
        engineer=current_user).order_by(Order.create_time.desc()).paginate(
        page, current_app.config['ORDERS_PER_PAGE'], False)
    return render_template('engineer/orders.html', title='工单列表',
                           orders=orders.items, pagination=orders)


@bp.route('/order_detail')
@login_required
def order_detail():
    order_id = request.args.get('id', 0, type=int)
    order = Order.query.filter_by(id=order_id).first_or_404()
    return render_template('engineer/order_detail.html', order=order)


@bp.route('/skill_view')
@login_required
def skill_view():
    page = request.args.get('page', 1, type=int)
    users = User.query.filter(User.role_id == 1).paginate(
        page, current_app.config['ORDERS_PER_PAGE'], False)
    return render_template(
        'engineer/skill_view.html', title='技能管理',
        pagination=users, users=users.items)


@bp.route('/skill_edit', methods=['GET', 'POST'])
@login_required
def skill_edit():
    form = SkillEditForm()
    user_id = request.args.get('id', 0, type=int)
    user = User.query.get(user_id)
    if user is None:
        flash('不存在的用户')
        return redirect(url_for('sales.skill_view'))
    if form.validate_on_submit():
        skill = Skills.query.filter_by(
            user=user,
            product=Product.query.get(form.product.data)).first()
        if skill is None:
            skill = Skills(
                user=user,
                product=Product.query.get(form.product.data))
            db.session.add(skill)
        skill.level = form.level.data
        db.session.commit()
        flash('技能[{}]更新完成'.format(skill.product.name))
        return redirect(url_for('engineer.skill_edit', id=user_id))
    skills = Skills.query.join(
        Product, Product.id == Skills.product_id).join(
        User, User.id == Skills.user_id).filter(
        Skills.user_id == user.id).all()
    return render_template(
        'engineer/skill_edit.html', title='技能管理',
        skills=skills, form=form, user=user)


@bp.route('/log_view')
@login_required
def log_view():
    log_id = request.args.get('log_id', 0, type=int)
    order_id = request.args.get('order_id', 0, type=int)
    log = Log.query.filter_by(id=log_id).first_or_404()
    order = Order.query.filter_by(id=order_id).first_or_404()
    return render_template(
        'engineer/log_detail.html', title='日志信息',
        log=log, order=order)


@bp.route('/write_log', methods=['GET', 'POST'])
@login_required
def write_log():
    form = LogForm()
    order_id = request.args.get('order_id', 0, type=int)
    order = Order.query.filter_by(id=order_id).first_or_404()
    if form.validate_on_submit():
        log = Log(
            title=form.title.data,
            content=form.content.data,
            begin=form.begin.data,
            after=form.after.data
        )
        order.logs.append(log)
        db.session.commit()
        flash('工作日志提交完成')
        return redirect(url_for('engineer.order_detail', id=order_id))
    return render_template(
        'engineer/write_log.html', title='填写日志', form=form,
        order=order)


@bp.route('/complete_order')
@login_required
def complete_order():
    order_id = request.args.get('order_id', 0, type=int)
    order = Order.query.filter_by(id=order_id).first_or_404()
    order.state_id = Code.finish
    result = Order.query.filter_by(engineer=current_user).filter(
        Order.state_id == Code.working).filter(
        Order.id != order.id).all()
    if result == []:
        current_user.state_id = Code.free
    db.session.commit()
    flash('您已确认完工')
    return redirect(url_for('engineer.order_detail', id=order_id))


@bp.route('/accept_order')
@login_required
def accept_order():
    order_id = request.args.get('order_id', 0, type=int)
    order = Order.query.filter_by(id=order_id).first_or_404()
    order.state_id = Code.working
    current_user.state_id = Code.busy
    db.session.commit()
    flash('您已接受工单')
    return redirect(url_for('engineer.order_detail', id=order_id))


@bp.route('/refuse_order')
@login_required
def refuse_order():
    order_id = request.args.get('order_id', 0, type=int)
    order = Order.query.filter_by(id=order_id).first_or_404()
    if order not in current_user.refused_records.all():
        current_user.refused_records.append(order)
        db.session.commit()
        flash('您已拒绝工单')
    if order.polling():
        db.session.commit()
    else:
        order.state_id = Code.refuse
        db.session.commit()
    return redirect(url_for('engineer.orders'))
