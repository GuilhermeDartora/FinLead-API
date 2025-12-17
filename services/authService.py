from models.user import User
from config import db

class AuthService:

    @staticmethod
    def register(nome, email, senha, role):
        #Verifica existencia de usuário
        user_existente = User.query.filter_by(email=email).first()
        if user_existente:
            raise ValueError("Usuário já existe")
        
        #cria usuário caso não exista
        user = User(
            nome=nome,
            email=email,
            role=role
        )
        user.setSenha(senha)

        #Salva no banco
        db.session.add(user)
        db.session.commit()

        return user
    
    @staticmethod
    def login(email, senha):
        user = User.query.filter_by(email=email).first()
        if not user or not user.checkSenha(senha):
            raise ValueError("Credenciais inválidas")
        
        return user