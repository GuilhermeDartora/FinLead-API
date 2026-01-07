from models.lead import Lead
from config import db


class LeadService:
    # Status permitidos (tu pode ajustar depois conforme teu fluxo)
    ALLOWED_STATUS = {"novo", "em_contato", "qualificado", "convertido", "perdido"}

    @staticmethod
    def _validate_lead_payload(data, is_update=False):
        if not isinstance(data, dict):
            raise ValueError("Body JSON inválido")

        nome = data.get("nome")
        email = data.get("email")
        telefone = data.get("telefone")
        status = data.get("status")

        # Nome obrigatório no create; opcional no update
        if not is_update:
            if not nome or not isinstance(nome, str) or not nome.strip():
                raise ValueError("O campo 'nome' é obrigatório e deve ser uma string")
        else:
            if nome is not None and (not isinstance(nome, str) or not nome.strip()):
                raise ValueError("O campo 'nome' deve ser uma string válida")

        if email is not None and not isinstance(email, str):
            raise ValueError("O campo 'email' deve ser uma string")

        if telefone is not None and not isinstance(telefone, str):
            raise ValueError("O campo 'telefone' deve ser uma string")

        if status is not None:
            if not isinstance(status, str):
                raise ValueError("O campo 'status' deve ser uma string")
            if status not in LeadService.ALLOWED_STATUS:
                raise ValueError(
                    f"Status inválido. Use um de: {', '.join(sorted(LeadService.ALLOWED_STATUS))}"
                )

    @staticmethod
    def calculate_score(nome, email, telefone, status):
        """
        Regra simples (MVP) — depois tu evolui com dados financeiros.
        - Base 10
        - +30 se tem telefone
        - +20 se tem email
        - +15 se status 'qualificado'
        - +25 se status 'convertido'
        - -10 se status 'perdido'
        """
        score = 10

        if telefone:
            score += 30
        if email:
            score += 20

        if status == "qualificado":
            score += 15
        elif status == "convertido":
            score += 25
        elif status == "perdido":
            score -= 10

        # garante 0..100
        score = max(0, min(100, score))
        return score

    @staticmethod
    def create_lead(data):
        LeadService._validate_lead_payload(data, is_update=False)

        nome = data.get("nome").strip()
        email = data.get("email")
        telefone = data.get("telefone")
        status = data.get("status") or "novo"

        # Evita duplicado (MVP) por email e/ou telefone, se informado
        if email:
            exists = Lead.query.filter_by(email=email).first()
            if exists:
                raise ValueError("Já existe um lead cadastrado com este email")

        if telefone:
            exists = Lead.query.filter_by(telefone=telefone).first()
            if exists:
                raise ValueError("Já existe um lead cadastrado com este telefone")

        score = LeadService.calculate_score(nome, email, telefone, status)

        lead = Lead(
            nome=nome,
            email=email,
            telefone=telefone,
            status=status,
            score=score
        )

        db.session.add(lead)
        db.session.commit()

        return lead

    @staticmethod
    def get_lead(lead_id):
        lead = Lead.query.get(lead_id)
        if not lead:
            raise LookupError("Lead não encontrado")
        return lead

    @staticmethod
    def list_leads(filters):
        """
        Filtros aceitos:
        - q: busca por nome/email/telefone (LIKE)
        - status: status exato
        - score_min: int
        - score_max: int
        - page: int (default 1)
        - per_page: int (default 10, máx 50)
        """
        q = filters.get("q")
        status = filters.get("status")
        score_min = filters.get("score_min")
        score_max = filters.get("score_max")

        page = filters.get("page", 1)
        per_page = filters.get("per_page", 10)

        try:
            page = int(page)
            per_page = int(per_page)
        except ValueError:
            raise ValueError("Parâmetros 'page' e 'per_page' devem ser inteiros")

        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 50:
            per_page = 50

        query = Lead.query

        if q:
            q_like = f"%{q}%"
            query = query.filter(
                (Lead.nome.ilike(q_like)) |
                (Lead.email.ilike(q_like)) |
                (Lead.telefone.ilike(q_like))
            )

        if status:
            if status not in LeadService.ALLOWED_STATUS:
                raise ValueError(
                    f"Status inválido. Use um de: {', '.join(sorted(LeadService.ALLOWED_STATUS))}"
                )
            query = query.filter(Lead.status == status)

        if score_min is not None:
            try:
                score_min = int(score_min)
            except ValueError:
                raise ValueError("score_min deve ser inteiro")
            query = query.filter(Lead.score >= score_min)

        if score_max is not None:
            try:
                score_max = int(score_max)
            except ValueError:
                raise ValueError("score_max deve ser inteiro")
            query = query.filter(Lead.score <= score_max)

        # ordena do mais recente
        query = query.order_by(Lead.created_at.desc())

        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            "items": [l.to_dict() for l in items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        }

    @staticmethod
    def update_lead(lead_id, data):
        LeadService._validate_lead_payload(data, is_update=True)

        lead = LeadService.get_lead(lead_id)

        if "nome" in data and data.get("nome") is not None:
            lead.nome = data.get("nome").strip()

        if "email" in data:
            new_email = data.get("email")
            if new_email != lead.email and new_email:
                exists = Lead.query.filter_by(email=new_email).first()
                if exists:
                    raise ValueError("Já existe um lead cadastrado com este email")
            lead.email = new_email

        if "telefone" in data:
            new_tel = data.get("telefone")
            if new_tel != lead.telefone and new_tel:
                exists = Lead.query.filter_by(telefone=new_tel).first()
                if exists:
                    raise ValueError("Já existe um lead cadastrado com este telefone")
            lead.telefone = new_tel

        if "status" in data and data.get("status") is not None:
            lead.status = data.get("status")

        # Recalcula score sempre que algo importante mudar (MVP)
        lead.score = LeadService.calculate_score(
            lead.nome,
            lead.email,
            lead.telefone,
            lead.status
        )

        db.session.commit()
        return lead

    @staticmethod
    def update_status(lead_id, new_status):
        if not new_status or not isinstance(new_status, str):
            raise ValueError("O campo 'status' é obrigatório e deve ser string")

        if new_status not in LeadService.ALLOWED_STATUS:
            raise ValueError(
                f"Status inválido. Use um de: {', '.join(sorted(LeadService.ALLOWED_STATUS))}"
            )

        lead = LeadService.get_lead(lead_id)
        lead.status = new_status

        # Recalcula score com base no novo status
        lead.score = LeadService.calculate_score(
            lead.nome,
            lead.email,
            lead.telefone,
            lead.status
        )

        db.session.commit()
        return lead
