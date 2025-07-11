from urllib.parse import quote_plus

FLASK_DEBUG=True
FLASK_RUN_PORT=5070
FLASK_APP="app"
ENV='prod'


# 数据库配置
DB_HOST='localhost'
DB_PORT='3306'
DB_USER='root'
DB_PWD=quote_plus('12345678')
DB_NAME='python_data_api'
DATABASE_URI='mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}?charset=utf8'.format(db_user=DB_USER, db_pwd=DB_PWD, db_host=DB_HOST, db_port=DB_PORT, db_name=DB_NAME)
DATABASE_SCHEMA=DB_NAME
DATABSE_PARAM_CHECK=True
DATABSE_ECHO=False

# 服务配置
SERVICE_HOST='http://localhost:5070'
PAGE_HOST='http://localhost:5173'
APP_NAME='DataApi'
SECRET_KEY='DataApiSecretKey'
RUNTIME_PATH='./runtime'

# 邮箱配置
SMTP_HOST = ""
SMTP_PORT = 465  # SSL端口
SMTP_USER = "noreply@*"  # 你的企业邮箱地址
SMTP_PASS = ""  # 邮箱密码或授权码
SMTP_SENDER = "noreply <noreply@*>"  # 发件人显示名称

# JDcloud短信模版
JD_REGION_ID = ''
JD_ACCESS_KEY = ''
JD_SECRET_KEY = ''
JD_SMS_CODE_TEMPLATE_ID = ''
JD_SMS_CODE_SIGN_ID = ''


