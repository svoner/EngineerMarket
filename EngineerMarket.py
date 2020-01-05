from app import create_app, db
from app.demo import Demo
from config import ProductionConfig
from app.models import (User, Role, State, Order, Product,
                        Log, Products, Skills, Code)

# 生产环境的配置
app = create_app(ProductionConfig)

# 开发环境的配置
# app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'State': State,
        'Order': Order,
        'Product': Product,
        'Log': Log,
        'Skills': Skills,
        'Products': Products,
        'Demo': Demo}


@app.cli.command()
def demo():
    # 初始化数据库
    db.drop_all()
    db.create_all()

    # 初始化基础数据
    User.insert_admin()
    Role.insert_roles()
    State.insert_state()

    # 插入演示数据
    Demo.insert_users()
    Demo.insert_products()
    Demo.insert_projects()
    Demo.insert_orders()
    Demo.insert_logs()
    Demo.insert_product_list()
    Demo.insert_skills()


@app.cli.command()
def deploy():
    # 初始化数据库
    db.drop_all()
    db.create_all()

    # 初始化基础数据
    Role.insert_roles()
    State.insert_state()
    User.insert_admin()
