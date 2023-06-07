from flask import Flask
from models.dao import Dao

app = Flask(__name__)
app.secret_key = '#$ab9&^BB00_.'

Dao = Dao(app)

from routes.login import user_view
from routes.dashboard import dashboard_view

app.register_blueprint(user_view)
app.register_blueprint(dashboard_view)
