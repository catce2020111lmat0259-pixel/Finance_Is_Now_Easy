from models.database import db


class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    valor = db.Column(db.Float, nullable=False)

    descricao = db.Column(db.String(200), nullable=True)

    data = db.Column(db.Date, nullable=False)

    recebido = db.Column(db.Boolean, default=False, nullable=False)

    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    categoria = db.relationship("Categoria", backref="receitas")

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    usuario = db.relationship("Usuario", backref="receitas")

    def validate(self):
        self.descricao = self.descricao.strip() if self.descricao else ""

        errors = []

        if not self.valor or self.valor <= 0:
            if "O valor da receita é obrigatório." not in errors:
                errors.append("O valor da receita é obrigatório.")

        if len(self.descricao) > 200:
            errors.append("A descrição deve ter no máximo 200 caracteres.")

        if not self.data:
            errors.append("A data da receita é obrigatória.")

        if not self.categoria_id:
            errors.append("Selecione uma categoria para a receita.")

        return errors

    def __repr__(self):
        return f"<Receita {self.id}: {self.descricao} - {self.valor}>"