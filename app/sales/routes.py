from app.sales import bp
from app.models import User, Project, Order, Role, Product, Products, Code
from app.sales.forms import OrderForm, ProductForm, ProjectForm, OrderCommentForm
from flask import redirect, url_for, render_template, request, current_app, flash
from flask_login import current_user, login_required
from datetime import datetime
from app import db


@bp.route('/index')
@login_required
def index():
    return redirect(url_for('sales.engineers'))


@bp.route('/engineers')
@login_required
def engineers():
    page = request.args.get('page', 1, type=int)
    users = User.query.filter(User.role_id==1).paginate(
        page, current_app.config['ENGINEERS_PER_PAGE'], False)
    return render_template(
        'sales/engineers.html', title='工程师列表',
        user=users.items, pagination=users)


@bp.route('/orders')
@login_required
def orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(
        sales=current_user).order_by(Order.create_time.desc()).paginate(
        page, current_app.config['ORDERS_PER_PAGE'], False)
    return render_template('sales/orders.html', title='派工历史',
                           orders=orders.items, pagination=orders)


@bp.route('/order_detail')
@login_required
def order_detail():
    order_id = request.args.get('id', 0, type=int)
    order = Order.query.filter_by(id=order_id).first_or_404()
    return render_template(
        'sales/order_detail.html', order=order,
        title='工单详情')


@bp.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    form = OrderForm()
    engineer_id = request.args.get('engineer_id', 0, type=int)
    if form.validate_on_submit():
        order = Order(
            title=form.title.data,
            description=form.description.data,
            working_hours=form.working_hours.data,
            state_id = Code.wait,
            begin_time=form.begin_time.data,
            project = Project.query.get(form.project.data),
            sales = current_user
        )
        if engineer_id == 0:
            if not order.polling():
                flash('该工单入场时间段内无可用工程师')
                db.session.rollback()
                return redirect('sales.index')
        else:
            order.engineer = User.query.get(engineer_id)
        db.session.add(order)
        for i in request.form.getlist('products'):
            p = Products(order=order, product=Product.query.get(int(i)))
            db.session.add(p)
        db.session.commit()
        flash('已将工单派发给工程师{}'.format(order.engineer.name))
        return redirect(url_for('sales.orders'))
    if engineer_id != 0:
        user = User.query.get(engineer_id)
        form.engineer.choices = [(user.id, user.name)]
    return render_template(
        'sales/place_order.html', title='派工', form=form)


@bp.route('/delete_order', methods=['GET', 'POST'])
@login_required
def delete_order():
    order_id = request.args.get('id', 0, type=int)
    order = Order.query.get(order_id)
    if order_id is None:
        flash('不存在的工单')
    else:
        for p in Products.query.filter_by(order=order).all():
            db.session.delete(p)
        db.session.delete(order)
        db.session.commit()
        flash('工单删除完成')
    return redirect(url_for('sales.orders'))


@bp.route('/products')
@login_required
def products():
    page = request.args.get('id', 1, type=int)
    products = Product.query.paginate(
        page, current_app.config['ORDERS_PER_PAGE'], False)
    return render_template(
        'sales/products.html',
        products=products.items,
        pagination=products,
        title='产品列表')


@bp.route('/edit_product', methods=['GET', 'POST'])
@login_required
def edit_product():
    product_id = request.args.get('id', 0, type=int)
    product = Product.query.get(product_id)
    if product is not None:
        form = ProductForm(product.name)
    else:
        form = ProductForm('')
    if form.validate_on_submit():
        if product is None:
            product = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data)
            db.session.add(product)
            db.session.commit()
            flash('产品{}添加成功'.format(product.name))
        else:
            product.name = form.name.data
            product.description = form.description.data
            product.price = form.price.data
            db.session.commit()
            flash('产品{}更新成功'.format(product.name))
        return redirect(url_for('sales.products'))
    if product is not None:
        form.name.data = product.name
        form.description.data = product.description
        form.price.data = product.price
    return render_template(
        'sales/edit_2pro.html', form=form,
        title='产品管理')


@bp.route('delete_product')
@login_required
def delete_product():
    product_id = request.args.get('product_id')
    product = Product.query.get(product_id)
    if product is None:
        flash('不存在的产品')
    else:
        db.session.delete(product)
        db.session.commit()
        flash('删除产品完成')
    return redirect(url_for('sales.products'))


@bp.route('/projects')
@login_required
def projects():
    page = request.args.get('id', 1, type=int)
    projects = Project.query.paginate(
        page, current_app.config['ORDERS_PER_PAGE'], False)
    return render_template(
        'sales/projects.html', projects=projects.items,
        pagination=projects, title='项目列表')


@bp.route('/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project():
    project_id = request.args.get('id', 0, type=int)
    project = Project.query.get(project_id)
    if project is not None:
        form = ProjectForm(project.name)
    else:
        form = ProjectForm('')
    if form.validate_on_submit():
        if project is None:
            project = Project(
                name=form.name.data,
                customer_name=form.customer_name.data,
                customer_phone=form.customer_phone.data,
                customer_address=form.customer_address.data,
                description=form.description.data
            )
            db.session.add(project)
            db.session.commit()
            flash('项目{}添加完成'.format(project.name))
        else:
            project.name = form.name.data
            project.customer_name = form.customer_name.data
            project.customer_phone = form.customer_phone.data
            project.customer_address = form.customer_address.data
            project.description = form.description.data
            db.session.commit()
            flash('项目{}更新成功'.format(project.name))
        return redirect(url_for('sales.projects'))
    if project is not None:
        form.name.data = project.name
        form.customer_name.data = project.customer_name
        form.customer_phone.data = project.customer_phone
        form.customer_address.data = project.customer_address
        form.description.data = project.description
    return render_template(
        'sales/edit_2pro.html', form=form,
        title='项目编辑')


@bp.route('delete_project')
@login_required
def delete_project():
    project_id = request.args.get('project_id')
    project = Product.query.get(project_id)
    if project is None:
        flash('不存在的产品')
    else:
        db.session.delete(project)
        db.session.commit()
        flash('删除产品完成')
    return redirect(url_for('sales.projects'))


@bp.route('/order_socre', methods=['GET', 'POST'])
@login_required
def order_score():
    order_id = request.args.get('id', 0, type=int)
    order = Order.query.filter_by(id=order_id).first_or_404()
    form = OrderCommentForm()
    if form.validate_on_submit():
        order.comment_score = form.score.data
        order.comment_time = datetime.utcnow()
        order.comment_content = form.content.data
        db.session.commit()
        flash('工单评价完成')
        return redirect(url_for('sales.order_detail', id=order_id))
    return render_template(
        'sales/order_score.html', order=order,
        title='工单评价', form=form)
