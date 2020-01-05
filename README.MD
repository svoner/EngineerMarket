# 系统的使用角色
本系统使用角色共分为三类，HR用于
1. HR
HR 类似于系统管理用， 用于管理使用系统的使用角色，包括添加用户、初始化用户密码、修改头像等
2. 工程师
工程师是使用系统的主要角色，技术主管可以管理每一位工程的技能，技能依赖于系统中存在的产品
3. 销售
销售是使用系统的主要角色，销售主管可以管理产品与项目。销售的实际派工过程依赖于项目和产品


# 运行环境的准备
## 下载程序
``` shell
git clone https://github.com/svoner/EngineerMarket
cd ./EngineerMarket
```

## 准备 Python 虚拟环境
``` shell
python3 -m venv venv
source venv/bin/activate
```
## 安装依赖库
```shell
(venv) pip install -r requirements.txt 
```
# 演示环境的部署
```shell
(venv) flask demo
```

使用用户名 user1-20 登录后，角色为 `工程师`。
使用用户名 user21-40 登录后，角色为 `销售`。
密码统一为 `user`

# 生产环境的部署
调整配置文件 config 中 ProductionConfig 部分的内容
```shell
(venv) flask deploy
```