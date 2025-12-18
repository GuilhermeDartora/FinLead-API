from flask import Blueprint, request
from services.authService import AuthService
from utils.response import success, error

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")
    role = data.get("role")

    try:
        user = AuthService.register(nome, email, senha, role)

        return success(
            "Usuário criado com sucesso",
            {
                "id": user.id,
                "nome": user.nome,
                "email": user.email,
                "role": user.role
            },
            201
        )

    except ValueError as e:
        return error(str(e), 400)

    except Exception:
        return error("Erro interno do servidor", 500)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    senha = data.get("senha")

    try:
        user = AuthService.login(email, senha)

        return success(
            "Login realizado com sucesso",
            {
                "id": user.id,
                "nome": user.nome,
                "email": user.email,
                "role": user.role
            }
        )

    except ValueError as e:
        return error(str(e), 401)

    except Exception:
        return error("Erro interno do servidor", 500)