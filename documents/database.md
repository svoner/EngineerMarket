# E-R 图

![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_log.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_refuse.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_products.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_skills.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_product.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_state.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_role.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_user.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_order.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_project.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_part_1.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_part_2.png?raw=true)
![](https://github.com/svoner/EngineerMarket/blob/master/documents/images/er_entirety.png?raw=true)


# 数据表描述

|编号|	中文名称|	表名|	描述|
| ------------ | ------------ | ------------ | ------------ |
1|		项目表|	Project|	存储可操作的所有项目信息
2|		派工单|	Order|	存储派工单的主表
3|		人员信息表|	User|	存储人员信息，通过角色编号区分人员角色
4|		工作日志|	Log|	存储工作日志
5|		人员角色|	Role|	存储角色的主表
6|		拒单记录|	Refused|	短期记录工程师拒单列表
7|		（服务）商品清单|	Products|	存储每张工单里所涉及到的产品
8|		技能表|	Skills|	存储每位工程师所拥有的技能星级信息
9|		产品表|	Product|	存储可操作的所有产品信息
10|		状态表|	State|	用于表示人员状态、工单状态


## 人员信息表（User）

|说明|	字段名|	数据类型|	长度|	允许空|	主键或索引|	约束|
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
编号|	id|	INT|		|NO|	主键|	
姓名|	name|	CHAR|	4|	NO|	索引|	唯一|
性别|	gender|	CHAR|	1|			
登录名|	user_name|	VARCHAR|	128|||			唯一|
密码散列|	password_hash|	VARCHAR|	128|			
电话|	phone|	VARCHAR|	20|			
邮箱|	email|	VARCHAR|	40|||			唯一|
头像链接|	avatar|	VARCHAR|	128	|		
状态编号|	state_id|	INT	|	|NO|	外键|	
担任主管|	is_manager|	BOOLEAN	|			
角色编号|	role_id|	TINYINT	|	|NO|	外键	|

## 项目表（Project）

|说明|	字段名|	数据类型|	长度|	允许空|	主键或索引|	约束|
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
编号|	id|	INT|		|NO|	主键|	
立项时间|	create_time|	DATETIME||||				2007年以后|
项目名称|	name|	VARCHAR|	15|	NO|	索引|	唯一|
描述|	description|	VARCHAR|	40|			
用户姓名|	customer_name|	CHAR|	4|			
用户电话|	customer_phone|	VARCHAR|	20|			
项目地址|	customer_address|	VARCHAR|	120|			


## 派工单（Order）

|说明|	字段名|	数据类型|	长度|	允许空|	主键或索引|	约束|
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
编号|	id|	INT|		|NO|	主键|	
创建时间|	create_time|	DATETIME|		|NO|		默认当前|
进场时间|	begin_time|	DATETIME|		|NO|		 
标题|	title|	VARCHAR|	15|	NO|	索引|	
描述|	description|	VARCHAR|	40|			
工时（天）|	working_hours|	INT|				
项目编号|	project_id|	INT|		|NO|	外键|	
销售编号|	sales_id|	INT|		|NO|	外键|	
技术编号|	engineer_id|	INT|		|NO|	外键|	
状态编号|	state_id|	INT|		|NO|	外键|	
评价分数|	comment_score|	INT||||				1=差，2=一般，3=好
评价时间|	comment_time|	DATETIME|				
评价内容|	comment_content|	VARCHAR|	200|			


## 工作日志（Log）
|说明|	字段名|	数据类型|	长度|	允许空|	主键或索引|	约束|
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
编号|	id|	INT|		|NO|	主键|	
标题|	title|	VARCHAR|	15|	NO|	索引|	
开始时间|	begin|	DATETIME|				
结束时间|	after|	DATETIME|				
内容|	content|	VARCHAR|	40|			
工单编号|	order_id|	INT|		|NO|	外键|	

## 技能表（Skills）
|说明|	字段名|	数据类型|	长度|	允许空|	主键或索引|	约束|
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
技术编号|	user_id|	INT|		|NO|	主键，外键|	
产品编号|	product_id|	INT|		|NO|	主键，外键|	
星级|	level|	INT|				
更新描述|	update_description|	VARCHAR|	50|			||默认空|

## 产品表（Product）
|说明|	字段名|	数据类型|	长度|	允许空|	主键或索引|	约束|
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
编号|	id|	INT|		|NO|	主键|	
产品名称|	name|	VARCHAR|	10|			
描述|	description|	VARCHAR|	40|			
基础价格|	price|	INT||||				1-2000|

## 商品清单（Products）
|说明|	字段名|	数据类型|	长度|	允许空|	主键或索引|	约束|
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
商品编号|	product_id|	INT|		|NO|	主键，外键|	
工单编号|	order_id|	INT|		|NO|	主键，外键|	
数量|	number|	INT||||				默认1|

## 角色表（Role）
|说明|	字段名|	数据类型|	长度|	允许空|	主键或索引|	约束|
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
编号|	id|	INT|		|NO|	主键|	
角色名称|	name|	VARCHAR|	5|

## 拒单表（refused）
|说明|	字段名|	数据类型|	长度|	允许空|	主键或索引|	约束|
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
技术编号|	user_id|	INT|		|NO|	主键，外键|	
工单编号|	order_id|	INT|		|NO|	主键，外键|

## 状态表（State）
|说明|	字段名|	数据类型|	长度|	允许空|	主键或索引|	约束|
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
编号|	id|	INT|		|NO|	主键|	
名称|	name|	VARCHAR|	5|	NO|		
名称|	name|	VARCHAR|	5|	NO|







