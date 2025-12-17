from config import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'gestor' ou 'vendedor'

    def setSenha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def checkSenha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<User {self.email} - {self.role}>"
