# doc
# blog-django
本项目使用后台使用的是python3.8.5 + Django2.2.15 + Django RestFramework3.11.0 + mysql 5.7.38 实现
## 调测方案：
1. git clone https://github.com/pycoder404/blog-django.git
2. cd blog-django
3. 编辑修改 Myblog/settings.py中的 DATABASES，根据真实情况修改为对应的数据库，调测过程中推荐使用mysql，如果使用mysql则需要在数据库中创建出对应的数据库（create database  dbname），dbname和配置中国你的dbname保持一致
4. 创建表
```bash
python manage.py makemigrations
python manage.py migrate
```
5. 启动调测服务器，**下面步骤启动的端口，[前端配置文件中的端口](http://127.0.0.1:8080/article/create)一致 **
```bash
python manage.py runserver 0:8080
```

6. 访问 http://127.0.0.1:8080验证是否启动成功
