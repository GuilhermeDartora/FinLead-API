from models.user import User
from config import db

class AuthService:

    @staticmethod
    def register(nome, email, senha, role):

        #Verifica campos obrigatórios
        if not nome or not email or not senha or not role:
            raise ValueError("Todos os campos são obrigatórios")
        
        #verifica tipos de dados
        if not isinstance(nome, str) or not isinstance(email, str) or not isinstance(senha, str) or not isinstance(role, str):
            raise ValueError("Tipos de dados inválidos")
        
        #tamanho mínimo da senha
        if len(senha) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres")
        
        #verfica formato do email
        if "@" not in email or "." not in email:
            raise ValueError("Formato de email inválido")
        
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