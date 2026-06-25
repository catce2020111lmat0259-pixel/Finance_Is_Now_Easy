from sqlalchemy import func

from models.database import db

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    tipo = db.Column(db.String(20), nullable=False)
    padrao = db.Column(db.Boolean, default=False, nullable=False)
    cor = db.Column(db.String(7), nullable=False, default="#585858")
    
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    usuario = db.relationship("Usuario", backref="categorias")

    def validate(self):
        self.nome = self.nome.strip() if self.nome else ""
        self.nome = " ".join(self.nome.split())
        self.tipo = self.tipo.strip() if self.tipo else ""
        self.descricao = self.descricao.strip() if self.descricao else ""
        self.cor = self.cor.strip() if self.cor else ""

        errors = []

        if not self.nome or self.tipo not in ["receita", "despesa"]:
            errors.append("O nome da categoria é obrigatório. Selecione se a categoria é Receita ou Despesa.")
            
        if len(self.nome) > 100:
            errors.append("A categoria deve ter no máximo 100 caracteres.")
            
        if len(self.descricao) > 200:
            errors.append("Descrição deve ter no máximo 200 caracteres.")
            
        categoria_existente = Categoria.query.filter(
            func.lower(Categoria.nome) == self.nome.lower(),
            Categoria.tipo == self.tipo,
            Categoria.usuario_id == self.usuario_id,
            Categoria.id != self.id
        ).first()

        if categoria_existente:
            errors.append("Já existe uma categoria com esse nome para esse tipo.")
            
        if len(self.cor) != 7 or not self.cor.startswith("#"):
            errors.append("A cor da categoria é inválida.")

        return errors

    def __repr__(self):
        return f"<Categoria {self.id}: {self.nome} ({self.tipo})>"