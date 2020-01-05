import random, shutil, os
from os import listdir
from app import db
from datetime import datetime, timedelta
from app.models import (User, Order, Role, State, Product, Project,
                        Log, Products, Skills, Code)


class Demo():
    @staticmethod
    def generate_name():
        xing = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
        ming = '豫章故郡洪都新府星分翼轸地接衡庐襟三江而婉月若华珠惠菱雪媛'
        while True:
            X = random.choice(xing)
            M = ''.join(random.choice(ming)
                        for i in range(random.randint(1, 2)))
            if User.query.filter_by(name=X+M).first() is None:
                return X+M

    @staticmethod
    def generate_phone():
        while True:
            phone = '13{}{:0>4d}{:0>4d}'.format(
                random.randrange(0, 9),
                random.randrange(0, 9999),
                random.randrange(0, 9999))
            if User.query.filter_by(phone=phone).first() is None:
                return phone

    @staticmethod
    def insert_users(count=40):
        avatar_list = './images'
        static_folder = './app/static'
        for i in os.listdir(static_folder):
            os.remove(os.path.join(static_folder, i))

        for i in os.listdir(avatar_list):
            shutil.copy(os.path.join(avatar_list, i),
                        os.path.join(static_folder, i))

        avatars = listdir('./app/static')

        for i in range(1, count):
            # 生成 user 演示数据
            u=User(
                name=Demo.generate_name(),
                gender=random.choice('男女'),
                username='user{}'.format(i),
                avatar=random.choice(avatars),
                phone=Demo.generate_phone(),
                email='user{}@gmail.com'.format(i),
                state_id=Code.free,
                is_manager=True
            )
            u.set_password('user')
            if i <= 20:
                u.role_id=Code.engineer
            else:
                u.role_id=Code.sales
            db.session.add(u)
        db.session.commit()

    @staticmethod
    def insert_products():
        # 生成产品演示数据
        p1=Product(
            name='上网行为管理',
            description='网康上网行为管理',
            price=300
        )
        p2=Product(
            name='防火墙',
            description='网神防火墙',
            price=400
        )
        p3=Product(
            name='入侵防御',
            description='网神入侵防御系统',
            price=550
        )
        db.session.add_all([p1, p2, p3])
        db.session.commit()

    @staticmethod
    def insert_projects():
        # 生成项目演示数据
        p1=Project(
            name='国家电网',
            customer_name='张经理',
            customer_phone='13212345565',
            customer_address='北京市宣武门西大街2号楼东'
        )
        p2=Project(
            name='中国海关总署',
            customer_name='刘科长',
            customer_phone='15322345567',
            customer_address='北京市建国门内大街6号'
        )
        p3=Project(
            name='神华集团',
            customer_name='陈队长',
            customer_phone='18988765534',
            customer_address='北京市西三环南路甲6号'
        )
        db.session.add_all([p1, p2, p3])
        db.session.commit()

    @staticmethod
    def insert_orders(count=50):
        # 生成工单演示数据
        for i in range(1, count):
            o=Order(
                title='演示工单{}'.format(i),
                description='演示工单描述数据',
                # 生成随机范围内的时间
                begin_time=datetime.utcnow(),
                working_hours=random.randint(1, 3),
                project=random.choice(Project.query.all()),
                engineer=random.choice(User.query.filter(
                    User.role_id == Code.engineer).all()),
                sales=random.choice(User.query.filter(
                    User.role_id == Code.sales).all()),
                state_id=random.choice(
                    [Code.wait, Code.working, Code.finish, Code.refuse])
            )
            if o.state_id == Code.working:
                o.engineer.state_id=Code.busy
            db.session.add(o)
        db.session.commit()

    @staticmethod
    def insert_logs(count=5):
        # 生成日志演示数据
        orders=Order.query.filter((Order.state_id == Code.finish) |
            (Order.state_id == Code.working)).all()
        for o in orders:
            for i in range(1, count):
                l=Log(
                    title='第{}天填写的工作日志'.format(i),
                    begin=datetime.utcnow() + timedelta(days=i),
                    after=datetime.utcnow() + timedelta(days=i),
                    content='第{}天工作日志的具体内容，该日志内容支持MD格式'.format(i),
                    order=o)
                db.session.add(l)
        db.session.commit()

    @staticmethod
    def insert_product_list():
        # 生成工单-产品演示数据
        products=Product.query.all()
        for o in Order.query.all():
            product_list=[]
            repeat_check=[]
            for i in range(1, products.__len__()):
                product=random.randint(1, products.__len__())
                if product not in repeat_check:
                    product_list.append(Products(order=o, product_id=product))
                    repeat_check.append(product)
            db.session.add_all(product_list)
        db.session.commit()

    @staticmethod
    def insert_skills():
        # 生成技能数据
        for u in User.query.filter_by(role_id=Code.engineer).all():
            for p in Product.query.all():
                skill=Skills(user=u, product=p)
                skill.level=random.randint(1, 5)
                db.session.add(skill)
        db.session.commit()
