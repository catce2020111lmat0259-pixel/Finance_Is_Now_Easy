import re

from models.database import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column( db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    pergunta_secreta = db.Column(db.String(50), nullable=False)
    resposta_secreta = db.Column(db.String(200), nullable=False)

    def validate(self):
        self.nome = self.nome.strip() if self.nome else ""
        self.email = self.email.strip() if self.email else ""
        self.senha = self.senha.strip() if self.senha else ""
        self.pergunta_secreta = self.pergunta_secreta.strip() if self.pergunta_secreta else ""
        self.resposta_secreta = self.resposta_secreta.strip() if self.resposta_secreta else ""

        errors = []

        # Nome
        if len(self.nome) < 3:
            errors.append("Tamanho do nome possui caracteres insuficientes. Minimo 3 caracteres.")
            
        if len(self.nome) > 100:
            errors.append("Tamanho do nome possui caracteres demais. Máximo 100 caracteres.")

        # Email
        padrao_email = r"^[a-zA-Z0-9._%+-]{3,}@[a-zA-Z0-9.-]{3,}\.[a-zA-Z.]{2,}$"
        dominios_permitidos = [
            "gmail.com",
            "hotmail.com",
            "outlook.com",
            "yahoo.com",
            "icloud.com",
            "uol.com.br",
            "bol.com.br",
            "ifpi.edu.br"
        ]

        if not re.match(padrao_email, self.email):
            errors.append("Informe um e-mail válido.")
        else:
            dominio = self.email.split("@")[1].lower()
            if dominio not in dominios_permitidos:
                errors.append("Use um domínio de e-mail válido, como gmail.com, hotmail.com, outlook.com ou ifpi.edu.br.")

        # Senha
        errors += self.validate_senha()
        
        # Data de nascimento
        if not self.data_nascimento:
            errors.append("Informe uma data de nascimento válida.")

        # Pergunta secreta
        if len(self.pergunta_secreta) < 3 or len(self.pergunta_secreta) > 100:
            errors.append("A pergunta secreta é inválida.")

        # Resposta secreta
        if len(self.resposta_secreta) < 2 or len(self.resposta_secreta) > 100:
            errors.append("A resposta secreta deve possuir entre 2 e 100 caracteres.")

        return errors
    
    def validate_senha(self):
        self.senha = self.senha.strip() if self.senha else ""

        errors = []

        if len(self.senha) < 6:
            errors.append("A senha deve possuir pelo menos 6 caracteres.")

        elif len(self.senha) > 100:
            errors.append("A senha deve possuir no máximo 100 caracteres.")

        elif not any(c.isupper() for c in self.senha) or not any(c.isdigit() for c in self.senha):
            errors.append("A senha deve possuir pelo menos uma letra maiúscula. E um número.")

        return errors

    def __repr__(self):
        return f"<Usuario {self.id}: {self.nome}>"