from flask import Flask
from flask_migrate import Migrate
from config import db, Config
from controllers.authController import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# REGISTRA O BLUEPRINT
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def home():
    return {"status": "API CRM rodando"}

if __name__ == "__main__":
    app.run(debug=True)
