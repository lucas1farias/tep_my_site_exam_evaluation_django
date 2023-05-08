

def projeto():
    """
    1. Crie um projeto Django chamado mysite
    """


class Accounts('App'):
    """
    2. Crie um app chamado accounts que utilize as funcionalidades django Auth e
       User

    a. deve realizar registro de usuários
        username, email, password

    b. deve realizar controle de login
        username, password
    """


class MyWallet('App'):
    """
    3. Crie um um app chamado my_wallet
    """


class Investor('modelo, primeiro modelo da app: my_wallet'):
    """
    a. Crie um modelo Investor que deve possuir uma relação um para um com User e funcione como o usuário de login.

    * as opções devem ser especificadas no modelo (choices)
    * perfil de risco (conservador, moderado, arrojado)
    """


class Stock('modelo, segundo modelo da app: my_wallet'):
    """
    b. Criar um modelo Stock para representar um ativo.

    * Código: 4 letras maiúsculas seguidas de um ou dois números (Ex: ITSA4 ou KLBL11)
    * Nome da empresa.
    * CNPJ da empresa: XX. XXX. XXX/0001-XX
    """


class StockAdd('criar objetos de: Stock'):
    """
    * cadastrar algumas stocks da bolsa de valores do brasil (B3): ex: ITSA4, WEGE3 etc.
    * OBS: não precisa criar view e template, pode ser feito pelo django admin.
    """


class Dashboard('template 1, página inicial, primeiro template da app: my_wallet'):
    """
    * Criar uma página "dashboard.html"
    * irá conter o resumo das posições de um usuário e deve ser a página inicial do app. (NÃO FEITO)
    * quantidade e valor total de cada ativo. (NÃO FEITO)
    """


class Transaction('modelo, terceiro modelo da app: my_wallet'):
    """
    * Criar um modelo para a classe Transaction com as seguintes propriedades:
        data                   || date
        stock                  || Stock ... relação n:1 (cada transaction é de um ativo, mas um ativo pode ter várias transações)
        quantidade de ações    || inteiro positivo
        preço unitário da ação || float positivo
        tipo de operação       || choices (C, compra, V, venda)
        corretagem             || float positivo
        investor               || Investor ... relação n:1 (cada operação é de um investor e um investor pode ter várias operações)
    """


class NewTransactions('template 2, formulário p/ criar nova transação, segundo template da app: my_wallet'):
    """
    e. Criar na página "dashboard.html" dois links:

        Cadastrar transação:
            Ir p/ uma página com um formulários p/ entrada dos dados p/ criar um objeto a partir do modelo Transaction
            O objeto de Transaction deve ser persistido no banco
            O banco é relacional (postgre, mysql, etc) ou mongodb
            Após o cadastro da operação deve ser retornado para a página "dashboard.html"
    """


class Transactions('template 3, template p/ exibição de transações criadas, terceiro template da app: my_wallet'):
    """
    * Criar um página "transactions.html"
    * Listar todas as operações do usuário em ordem crescente de data (da mais antiga em cima p/ a mais recente embaixo)
    * Deve conter um campo para filtrar operações por código da ação. (NÃO FEITO) (Botão de pesquisa?)
    * Deve conter um botão de “voltar” que leva para "dashboard.html"

    * Para visualização de cada operação calcular e exibir os valores: (NÃO FEITO a parte de calcular apenas)
        1. Código do ativo 2. Tipo de operação (compra ou venda) 3. Data 4. Quantidade 5. Preço unitário 6. Total

    * Para cada operação deve haver um botao para detalhar a operação que abre uma página "detalhe.html" (NÃO FEITO)
    """


class Detalhe('template 4, template p/ exibição de detalhes sobre cada transação, quarto template da app: my_wallet'):
    """
    * Continuação da parte acima
    * Para cada operação deve haver um botão para detalhar a operação que abre uma página "detalhe.html"
    * Criar uma página "detalhe.html" para detalhar uma transação específica.

        * Deve ser possível editar ou remover a operação e voltar para a página "transactions.html"
        * Para cada ação deve ser exibido mensagem(ns) de sucesso ou erro(s)
        * Deve ser aplicado a reutilização de templates.
        * Deve ser aplicado estilização css e, se necessário, scripts e imagens.

        Opcional e adicional: utilização de Django Forms.

        * ======= Como realizar os cálculos =======
        ● quantidade de ações (Q)
        ● custo unitário da ação (U)
        ● custo de corretagem (C)
        ● valor de compra (V) = Q * U
        ● taxas B3 = B
        ● taxas_totais (T) = B + C
        ● valor total da negociação (X)
        ● se for operação de compra: X = V + T
        ● se for operação de venda: X = V - T
    """
