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
- O sistema deve agrupar automaticamente as despesas por categoria.
- O sistema deve exibir o total e o percentual gasto em cada categoria.
- O sistema deve permitir filtragem por mês e ano.
- O sistema deve utilizar essas informações nos gráficos financeiros.

## HU06 - Relatório mensal
- O sistema deve gerar um relatório financeiro em PDF.
- O relatório deve apresentar receitas, despesas e saldo do período.
- O relatório deve incluir uma análise automática da situação financeira.
- O relatório deve apresentar gráfico comparativo e resumo mensal.
- O relatório deve conter todos os lançamentos do período selecionado.

## HU07 - Gráficos
- O sistema deve gerar gráficos de pizza para receitas e despesas.
- O sistema deve utilizar as cores personalizadas das categorias.
- O sistema deve apresentar legenda, valores e percentuais.
- O sistema deve informar quando não existirem dados para o período.

## HU08 - Comparativo mensal
- O sistema deve comparar receitas, despesas e saldo entre os meses.
- O sistema deve permitir seleção do ano.
- O sistema deve apresentar gráfico comparativo e tabela anual.
- O sistema deve informar quando não existirem registros.

## HU09 - Metas financeiras
- O sistema deve permitir criar metas financeiras.
- O sistema deve listar metas cadastradas.
- O sistema deve permitir editar metas.
- O sistema deve permitir excluir metas.
- O sistema deve permitir definir uma meta principal para exibição na Dashboard.

## HU10 - Avisos de orçamento
- O sistema deve identificar automaticamente despesas pendentes.
- O sistema deve identificar receitas não recebidas.
- O sistema deve atualizar os avisos automaticamente.
- O sistema deve informar quando não existirem pendências.

## HU11 - Dashboard
- O sistema deve apresentar a meta principal.
- O sistema deve apresentar avisos financeiros.
- O sistema deve apresentar as últimas movimentações.

## HU12 - Interface responsiva
- O sistema deve se adaptar a diferentes tamanhos de tela.
- O sistema deve manter navegação acessível e intuitiva.
- O sistema deve exibir feedback visual das ações do usuário.

## HU13 - Filtros
- O sistema deve permitir pesquisa textual.
- O sistema deve permitir navegação entre meses.
- O sistema deve atualizar automaticamente os resultados.
- O sistema deve informar quando não existirem registros.

## HU14 - Persistência de dados
- O sistema deve salvar dados automaticamente.
- O sistema deve recuperar dados ao reiniciar.
- O sistema deve garantir integridade dos dados após login.

## HU15 - Login e autenticação
- O sistema deve permitir autenticação de usuários.
- O sistema deve restringir acesso a usuários autenticados.
- O sistema deve proteger os dados do usuário.