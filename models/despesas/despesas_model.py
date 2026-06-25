from models.database import db


class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    data = db.Column(db.Date, nullable=False)
    pago = db.Column(db.Boolean, default=False, nullable=False)

    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    categoria = db.relationship("Categoria", backref="despesas")

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    usuario = db.relationship("Usuario", backref="despesas")

    def validate(self):
        self.descricao = self.descricao.strip() if self.descricao else ""

        errors = []

        if not self.valor or self.valor <= 0:
            if "O valor da despesa é obrigatório." not in errors:
                errors.append("O valor da despesa é obrigatório.")

        if len(self.descricao) > 200:
            errors.append("A descrição deve ter no máximo 200 caracteres.")

        if not self.data:
            errors.append("A data da despesa é obrigatória.")

        if not self.categoria_id:
            errors.append("Selecione uma categoria para a despesa.")

        return errors

    def __repr__(self):
        return f"<Despesa {self.id}: {self.descricao} - {self.valor}>"