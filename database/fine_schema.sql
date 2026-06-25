CREATE DATABASE fine;
USE fine;

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    pergunta_secreta VARCHAR(150) NOT NULL,
    resposta_secreta VARCHAR(150) NOT NULL
);

CREATE TABLE categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(200),
    tipo ENUM('receita', 'despesa') NOT NULL,
    cor VARCHAR(20) NOT NULL DEFAULT '#2563eb',
    padrao BOOLEAN NOT NULL DEFAULT FALSE,
    usuario_id INT NOT NULL,

    CONSTRAINT fk_categoria_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON DELETE CASCADE
);

CREATE TABLE receita (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valor DECIMAL(10,2) NOT NULL,
    data DATE NOT NULL,
    descricao VARCHAR(200),
    recebido BOOLEAN NOT NULL DEFAULT FALSE,

    usuario_id INT NOT NULL,
    categoria_id INT NOT NULL,

    CONSTRAINT fk_receita_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_receita_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES categoria(id)
);

CREATE TABLE despesa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valor DECIMAL(10,2) NOT NULL,
    data DATE NOT NULL,
    descricao VARCHAR(200),
    pago BOOLEAN NOT NULL DEFAULT FALSE,

    usuario_id INT NOT NULL,
    categoria_id INT NOT NULL,

    CONSTRAINT fk_despesa_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_despesa_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES categoria(id)
);

CREATE TABLE meta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conteudo VARCHAR(200) NOT NULL,
    fixada BOOLEAN NOT NULL DEFAULT FALSE,

    usuario_id INT NOT NULL,

    CONSTRAINT fk_meta_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON DELETE CASCADE
);