from flask import Flask
from config import db, Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route("/")
def home():
    return {"status": "API CRM rodando"}

if __name__ == "__main__":
    app.run(debug=True)
