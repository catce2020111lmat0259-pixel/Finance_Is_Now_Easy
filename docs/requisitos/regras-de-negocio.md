# Regras de Negócio

## HU01 - Inserir receitas manualmente
- O sistema deve permitir cadastrar receitas com valor, data e categoria.
- O sistema deve validar o preenchimento dos campos obrigatórios.
- O sistema deve impedir o cadastro de valores inválidos ou negativos.

## HU02 - Inserir despesas manualmente
- O sistema deve permitir cadastrar despesas com valor, data e categoria.
- A categoria deve ser obrigatória no cadastro.
- O sistema deve impedir o cadastro com valores inválidos.

## HU03 - Editar e excluir lançamentos
- O sistema deve permitir editar lançamentos existentes.
- O sistema deve permitir excluir lançamentos.
- O sistema deve solicitar confirmação antes da exclusão.

## HU04 - Classificação por categorias
- O sistema deve permitir associar categorias aos lançamentos.
- O sistema deve disponibilizar categorias pré-definidas.
- O sistema deve permitir criar novas categorias.

## HU05 - Resumo por categoria
- O sistema deve agrupar despesas por categoria.
- O sistema deve exibir o total gasto por categoria.
- O sistema deve permitir filtragem por período.

## HU06 - Relatório mensal
- O sistema deve exibir relatório com receitas, despesas e saldo.
- O sistema deve permitir exportar dados (CSV ou PDF).
- O relatório deve conter todos os lançamentos do período.

## HU07 - Gráficos
- O sistema deve exibir gráficos de pizza e/ou barras por categoria.
- O sistema deve apresentar visualização proporcional dos gastos.
- O sistema deve informar quando não houver dados disponíveis.

## HU08 - Comparativo mensal
- O sistema deve exibir comparativo de gastos entre meses.
- O sistema deve permitir filtro por período.
- O sistema deve informar quando não houver registros no período.

## HU09 - Metas financeiras
- O sistema deve permitir criar metas financeiras personalizadas.
- O sistema deve listar metas cadastradas.
- O sistema deve permitir editar metas.
- O sistema deve permitir excluir metas.
- O sistema deve exibir o status das metas (em andamento, concluída, não atingida).

## HU10 - Avisos de orçamento
- O sistema deve alertar quando o limite de orçamento for ultrapassado.
- O sistema deve emitir aviso preventivo ao atingir percentual do limite.
- O sistema deve indicar quando não houver limite definido.

## HU11 - Dashboard
- O sistema deve exibir saldo atual, receitas e despesas.
- O sistema deve exibir valores zerados quando não houver dados.
- O sistema deve atualizar os dados automaticamente.

## HU12 - Interface responsiva
- O sistema deve se adaptar a diferentes tamanhos de tela.
- O sistema deve manter navegação acessível e intuitiva.
- O sistema deve exibir feedback visual das ações do usuário.

## HU13 - Filtros
- O sistema deve permitir filtro por categoria.
- O sistema deve permitir filtro por período.
- O sistema deve informar quando não houver resultados.

## HU14 - Personalização
- O sistema deve permitir alterar cores da interface.
- O sistema deve exibir prévia das alterações.
- O sistema deve permitir restaurar o padrão.

## HU15 - Persistência de dados
- O sistema deve salvar dados automaticamente.
- O sistema deve recuperar dados ao reiniciar.
- O sistema deve garantir integridade dos dados após login.

## HU16 - Login e autenticação
- O sistema deve permitir autenticação de usuários.
- O sistema deve restringir acesso a usuários autenticados.
- O sistema deve proteger os dados do usuário.