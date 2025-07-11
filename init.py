import subprocess
import os
import sys
import pymysql
import env
import json

# 1. 安装 Python 依赖
def install_python_requirements():
    req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_file):
        print("正在安装 Python 依赖...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_file])
    else:
        print("未找到 requirements.txt，跳过 Python 依赖安装。")

# 2. 安装前端依赖
def install_npm_packages():
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    pkg_file = os.path.join(static_dir, 'package.json')
    if os.path.exists(pkg_file):
        print("正在安装前端依赖（npm install）...")
        subprocess.check_call(['npm', 'install'], cwd=static_dir)
    else:
        print("未找到 static/package.json，跳过 npm install。")

def init_database():
    # 2. 连接数据库
    conn = pymysql.connect(
        host=env.DB_HOST,
        port=int(env.DB_PORT),
        user=env.DB_USER,
        password=env.DB_PWD,
        database=env.DB_NAME,
        autocommit=True
    )
    cursor = conn.cursor()

    admin_token = env.ADMIN_TOKEN

    # 3. 执行 SQL 脚本
    sql_path = os.path.join(os.path.dirname(__file__), 'conf/python_data_api.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    sql_script = sql_script.replace('{{ADMIN_TOKEN}}', admin_token)
    
    for statement in sql_script.split(';'):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)

    # 4. 更新 workflow_db 的 meta 字段
    # 假设你要更新 id=1 的 meta 字段为 '{"init": true}'
    update_sql = "UPDATE datain SET meta=%s WHERE id=1 and code='workflow_db'"

    meta = {
        "dev":{
            "db_type":"mysql",
            "db_host":env.DB_HOST,
            "db_name":env.DB_NAME,
            "db_port":env.DB_PORT,
            "db_user":env.DB_USER,
            "db_pwd" :env.DB_PWD
        },
        "prod":{
            "db_type":"mysql",
            "db_host":env.DB_HOST,
            "db_name":env.DB_NAME,
            "db_port":env.DB_PORT,
            "db_user":env.DB_USER,
            "db_pwd" :env.DB_PWD
        }
    }
    cursor.execute(update_sql, (json.dumps(meta),))

    cursor.close()
    conn.close()
    print("数据库初始化完成。")

if __name__ == "__main__":
    install_python_requirements()
    install_npm_packages()
    init_database()

