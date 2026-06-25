from models.database import db

class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    fixada = db.Column(db.Boolean, default=False, nullable=False)
    usuario = db.relationship("Usuario", backref="metas")

    def validate(self):
        self.conteudo = self.conteudo.strip() if self.conteudo else ""
        errors = []

        if not self.conteudo:
            errors.append("A meta é obrigatória e não pode ser vazia.")

        if len(self.conteudo) < 2:
            errors.append("Mínimo 2 caracteres.")
            
        if len(self.conteudo) > 200:
            errors.append("Máximo 200 caracteres.")

        return errors

    def __repr__(self):
        return f"<Meta {self.id}: {self.conteudo}>"