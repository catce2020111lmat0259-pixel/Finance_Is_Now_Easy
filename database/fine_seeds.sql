USE fine;

-- Exemplo de Usuário (fine)
INSERT INTO usuario (
    nome,
    email,
    senha,
    data_nascimento,
    pergunta_secreta,
    resposta_secreta
) VALUES (
    'Gabriel Lopes da Silva',
    'gabriel@fine.com',
    '$2b$12$EXEMPLOHASHDASENHA',
    '2002-03-02',
    'Nome da cidade em que nasceu?',
    'Teresina'
);

-- Categorias de Receita
INSERT INTO categoria (nome, descricao, tipo, cor, padrao, usuario_id) VALUES
('Salário', 'Recebimento mensal', 'receita', '#22c55e', TRUE, 1),
('Freelance', 'Trabalhos extras', 'receita', '#16a34a', TRUE, 1),
('Investimentos', 'Rendimentos financeiros', 'receita', '#0f766e', TRUE, 1),
('Outros', 'Outras entradas', 'receita', '#15803d', TRUE, 1);

-- Categorias de Despesa
INSERT INTO categoria (nome, descricao, tipo, cor, padrao, usuario_id) VALUES
('Alimentação', 'Mercado e refeições', 'despesa', '#ef4444', TRUE, 1),
('Transporte', 'Combustível e transporte público', 'despesa', '#f97316', TRUE, 1),
('Lazer', 'Cinema, viagens e entretenimento', 'despesa', '#e11d48', TRUE, 1),
('Outros', 'Demais despesas', 'despesa', '#dc2626', TRUE, 1);

-- Meta de exemplo
INSERT INTO meta (conteudo, fixada, usuario_id)
VALUES (
    'Guardar R$ 5.000,00 até o final do ano',
    TRUE,
    1
);