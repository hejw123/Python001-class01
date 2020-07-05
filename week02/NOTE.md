# 第二周学习笔记 

## Python - 连接数据库（mysql）
### pymysql
#### 打开数据库连接 
DB = pymysql.connect("IP","USER","PASSWORD","DATABASE")
#### 执行SQL语句
DB.execute(SQL)
#### 使用cursor()方法 开启事务
cursor = DB.cursor()
#### 提交事务
DB.commit()
#### 回滚事务
DB.rollback()

## Python - 模拟浏览器
## WebDriver
使用浏览器的功能来模拟登陆，获取header

## Python - 分布式爬虫
通信中间价 - redis
队列通信 
