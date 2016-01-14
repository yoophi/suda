import os

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.config import Config
from suda.models import db, Post, User, Token

from suda.models import Client

app = Flask(__name__)
config = Config(app)
admin = Admin(app)
db.init_app(app)

app.config.from_yaml(search_paths=('/etc/suda', os.path.dirname(os.path.dirname(app.root_path))))

@app.route('/')
def index():
    return 'hello world'

admin.add_view(ModelView(Client, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Token, db.session))

if __name__ == '__main__':
    app.run(debug=True)