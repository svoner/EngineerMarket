from app import db, login
from datetime import datetime
from flask_login import UserMixin, current_user
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import timedelta


class Code():
    engineer = 1  # 工程师
    sales = 2     # 销售
    hr = 3        # 人事（管理员）
    free = 1      # 在岗
    vacation = 2  # 请假
    busy = 3      # 出工
    wait = 4      # 等待接单
    refuse = 5    # 退单
    finish = 6    # 已完成
    working = 7   # 实施中
    bad = 1       # 差评
    middle = 2    # 中评
    good = 3      # 好评


class Products(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(
        db.Integer, db.ForeignKey('product.id'), primary_key=True)
    order_id = db.Column(
        db.Integer, db.ForeignKey('order.id'), primary_key=True)
    number = db.Column(db.Integer, default=1)
    product = db.relationship(
        'Product', backref='orders',)
    order = db.relationship(
        'Order', backref='products',)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4), unique=True)
    gender = db.Column(db.String(1))
    username = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(128), index=True, unique=True)
    avatar = db.Column(db.String(128))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    is_manager = db.Column(db.Boolean, default=False)
    refused_records = db.relationship(
        'Order',
        secondary='refused',
        lazy='dynamic'
    )

    @staticmethod
    def insert_admin():
        user = User(
            name='管理员',
            username='admin',
            role_id=Code.hr
        )
        user.set_password('admin')
        db.session.add(user)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_skills(self):
        skills = Skills.query.join(
            Product, Product.id == Skills.product_id).join(
            User, User.id == Skills.user_id).filter(
            Skills.user_id == self.id).all()
        return skills

    def get_state_name(self):
        return State.query.filter(State.id == self.state_id).first().name

    def get_state_class(self):
        if self.state_id == Code.free:
            return 'success'
        if self.state_id == Code.busy:
            return 'warning'

    def get_index(self):
        if self.role.name == 'engineer':
            return 'engineer.index'
        if self.role.name == 'sales':
            return 'sales.index'
        if self.role.name == 'hr':
            return 'hr.index'

    def count_orders(self):
        orders = db.session.query(
            Order, func.count(Order.id)).filter(
                Order.sales_id == current_user.id).first()[1]
        return orders

    def count_hours(self):
        self.hours = db.session.query(
            Order, func.sum(Order.working_hours)).filter(
                Order.sales_id == current_user.id).first()[1]
        return self.hours

    def totle_price(self):
        totle = 0
        orders = Order.query.filter_by(sales=self).all()
        if orders is not None:
            for o in orders:
                if o.state_id == Code.refuse:
                    continue
                totle += o.calc_price()
        return totle

    def __repr__(self):
        return '<User> {}'.format(self.name)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role> {}'.format(self.name)

    @staticmethod
    def insert_roles():
        for r in ['engineer', 'sales', 'hr']:
            data = Role(name=r)
            db.session.add(data)
            db.session.commit()


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), unique=True)
    users = db.relationship('User', backref='state', lazy='dynamic')
    orders = db.relationship('Order', backref='state', lazy='dynamic')

    def __repr__(self):
        return '<State> {}'.format(self.name)

    @staticmethod
    def insert_state():
        state_list = ['在岗', '请假', '出工',
                      '等待接单', '退单', '已完成', '实施中']
        for s in state_list:
            data = State(name=s)
            db.session.add(data)
            db.session.commit()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime)
    name = db.Column(db.String(40), index=True, unique=True)
    description = db.Column(db.String(40))
    customer_name = db.Column(db.String(4))
    customer_phone = db.Column(db.String(20))
    customer_address = db.Column(db.String(120))
    orders = db.relationship('Order', backref='project', lazy='dynamic')

    def __repr__(self):
        return '<Project> {}'.format(self.name)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    begin_time = db.Column(db.DateTime)
    title = db.Column(db.String(15))
    description = db.Column(db.String(40))
    working_hours = db.Column(db.Integer, default=0)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    engineer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sales_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    comment_score = db.Column(db.Integer)
    comment_time = db.Column(db.DateTime)
    comment_content = db.Column(db.String(200))
    engineer = db.relationship(
        'User',
        foreign_keys='Order.engineer_id',
        backref=db.backref('achivements', order_by='Order.begin_time.desc()'))
    sales = db.relationship(
        'User',
        foreign_keys='Order.sales_id',
        backref='orders')
    refused_engineers = db.relationship(
        'User',
        secondary='refused',
        lazy='dynamic'
    )

    logs = db.relationship('Log', backref='order', lazy='dynamic')

    def polling(self):
        # 1. 按指定时间轮询派发工单给`free`状态的工程师
        # 2. 没有`free`可用查找所有`busy`状态的工程师
        # 3. 对`busy`工程师做忙时冲突检测，一旦检测通过即派给该同事
        who_refused = [i.id for i in self.refused_engineers.all()]
        users = User.query.filter(
            User.state_id == Code.free).filter(
                ~User.id.in_(who_refused)).all()
        if users is not None:
            self.engineer = random.choice(users)
            return True
        users = User.query.filter(
            User.state_id == Code.busy).filter(
                ~User.id.in_(who_refused)).all()
        if users is not None:  # 忙时冲突检测
            for u in users:
                for o in u.achivements:
                    if (o.state_id == Code.working and
                            self.begin_time > o.begin_time + timedelta(days=o.working_hours)):
                        self.engineer = u
                        return True
        return False

    def add_product(self, product):
        self.products.append(product)

    def formated_create_time(self):
        return self.create_time.strftime('%Y年%m月%d日')

    def calc_price(self):
        price = 0
        index = 1
        products = Product.query.join(
            Products, Products.product_id == Product.id).filter(
                Products.order_id == self.id).order_by(
                    Product.price.desc()).all()
        if products is None:
            return 0
        for p in products:
            if index == 1:
                price = price + p.price
            if index == 2:
                price = price + p.price * 0.75
            if index >= 3:
                price = price + p.price * 0.5
            index += 1
        return price * self.working_hours

    def get_products(self):
        products = Product.query.join(
            Products, Products.product_id == Product.id).join(
                Order, Products.order_id == Order.id).filter(
                    Order.id == self.id).all()
        return products

    def get_state_class(self):
        if self.state_id == Code.refuse:
            return 'danger'
        if self.state_id == Code.wait:
            return 'warning'
        if self.state_id == Code.finish:
            return 'success'

    def get_score_str(self):
        if self.comment_score == Code.bad:
            return '差'
        elif self.comment_score == Code.middle:
            return '一般'
        elif self.comment_score == Code.good:
            return '好'
        else:
            return ''

    def __repr__(self):
        return '<Order> {}'.format(self.title)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    description = db.Column(db.String(40))
    price = db.Column(db.Integer)

    def __repr__(self):
        return '<Product> {}'.format(self.name)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(15))
    begin = db.Column(db.DateTime)
    after = db.Column(db.DateTime)
    content = db.Column(db.String(200))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __repr__(self):
        return '<WorkLog> {}'.format(self.title)


refused = db.Table(
    'refused',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id'), primary_key=True),
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True))


class Skills(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), primary_key=True)
    level = db.Column(db.SmallInteger)
    update_description = db.Column(db.String(50), default='')
    user = db.relationship(
        'User'
    )
    product = db.relationship(
        'Product'
    )


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
