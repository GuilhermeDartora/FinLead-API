from flask import Flask
from flask_migrate import Migrate
from config import db, Config
from controllers.authController import auth_bp
from controllers.leadController import lead_bp
from models.user import User
from models.lead import Lead


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# REGISTRA O BLUEPRINT
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(lead_bp, url_prefix="/leads")

@app.route("/")
def home():
    return {"status": "API CRM rodando"}

if __name__ == "__main__":
    app.run(debug=True)
