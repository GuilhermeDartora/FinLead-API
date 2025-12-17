from flask import Flask
from flask_migrate import Migrate
from config import db, Config
from models.user import User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# 🔹 REGISTRA O FLASK-MIGRATE
migrate = Migrate(app, db)

@app.route("/")
def home():
    return {"status": "API CRM rodando"}

if __name__ == "__main__":
    app.run(debug=True)
