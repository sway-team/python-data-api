from flask import Flask,redirect
from flask_cors import CORS
import env,os
from api.dataset import router as dataset_router
from api.user import router as user_router
from api.frame import router as frame_router
from api.service import router as service_router

app = Flask(__name__)
app.secret_key = env.SECRET_KEY  # 添加secret key配置

CORS(app, resources={
    "/*": {
        "origins": ["http://localhost:5173"],  # Allow only your frontend origin
        "methods": ["GET", "POST", "OPTIONS"],  # Allowed methods
        "allow_headers": ["Content-Type", "Authorization"],  # Allowed headers
        "supports_credentials": True  # Enable credentials support for session
    }
})

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
globals()['app'] = app
app.config.from_object(env)

@app.route("/")

def hello_world():
    print('ok')
    return {'result':'ok'}

@app.route('/app/<path:subpath>')
def serve_app_catchall(subpath):
    return redirect(env.PAGE_HOST + '/app/' + subpath)


app.register_blueprint(dataset_router, url_prefix='/dataset')
app.register_blueprint(user_router, url_prefix='/user')
app.register_blueprint(frame_router, url_prefix='/frame')
app.register_blueprint(service_router, url_prefix='/service')

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, threaded=True, port=env.FLASK_RUN_PORT)

# create a new orm object
# sqlalchemy.exc.ObjectNotExecutableError: Not an executable object: 'SELECT * from dataset'

