

/*
1. I have these models and they have a relationship

class Stock(Base):
    code = models.CharField('Código', max_length=6)
    company_name = models.CharField('Nome da empresa', max_length=150)
    corporate_taxpayer_registry = models.CharField('CNPJ da empresa', max_length=18)

    def __str__(self):
        return self.code
class Transaction(Base):
    OPERATION_CHOICES = (
        ('c', 'compra'),
        ('v', 'venda'),
    )

    creation_date = models.CharField('Data de criação do Ativo', max_length=10)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)  # objeto.code (vindo de Stock)
    stock_shares = models.SmallIntegerField('Quantidade de ações')
    share_unit_price = models.DecimalField('Preço unitário da ação', max_digits=8, decimal_places=2)
    operation = models.CharField('Tipo da operação', max_length=1, choices=OPERATION_CHOICES)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)

    def __str__(self):
        return self.stock.code

2. I have this view

class NewTransactionView(CreateView):
    template_name = 'new_transaction.html'
    model = Transaction
    fields = ('stock', 'stock_shares', 'share_unit_price', 'operation', 'investor')

    def post(self, request):
        if str(request.method) == 'POST':

            new_transaction = create_object(
                label='transaction',
                db=NewTransactionView.model,
                fields=(
                    request.POST.get('creation_date'),
                    request.POST.get('stock'),      # dropdowns
                    request.POST.get('stock_shares'),
                    request.POST.get('share_unit_price'),
                    request.POST.get('operation'),  # dropdowns
                    request.POST.get('investor')    # dropdowns
                )
            )
            new_transaction.save()
            success(request, 'Nova transação adicionada!')
            return redirect('dashboard')

3. I have a template with all the inputs that are retrieved inside the "post" function inside the "NewTransactionView" view
4. When I try to create a new transaction, I get an error
5. When I select one of the stocks from the <select> <option> tag, Django says: "Cannot assign "'FUSS84'": "Transaction.stock" must be a "Stock" instance.
6. 'FUSS84', in this context, is one among many dropdowns resulting from the iteration over the model "Stock" found at "NewTransactionView" through the variable "context['stocks'] = call_model(Stock)"

<!-- my_wallet/models.py/Transaction/stock -->
    <div class="flex-column black-cover">
        <div>
            <p>Escolher a ação</p>
        </div>
        <select class="select-config" name="stock">
            <option>escolher ação...</option>
            {% for stock in stocks %}
                <option value="{{ stock.code }}">{{ stock.code }}</option>
            {% endfor %}
        </select>
    </div>

7. The error specifies that I am passing only a string, which must be coming from the "def __str__(self): return self.stock.code" inside the "Transaction" model
8. I do not understand how I should be passing the entire instance of "Stock" 
9. How can I fix this?
*/

/*
1. I have two models related by a ForeignKey in Django (Stock gives the inheritance to Transaction)
2. The model that receives the inheritance will be setup like: field = models.ForeignKey(Stock)
3. When I try to create a transaction object
*/

/*
1. Eu tenho uns cálculos para fazer numa aplicação Django
2. O problema é que a pessoa que me passou as instruções, não passou elas de forma clara
3. Aqui está a demonstração

● quantidade de ações (Q)    
● custo unitário da ação (U)    
● custo de corretagem (C)
● valor de compra (V) = Q * U (FEITO)
● taxas B3 = B
● taxas_totais (T) = B + C
● valor total da negociação (X)
● se for operação de compra: X = V + T
● se for operação de venda: X = V - T

4. No projeto que me foi passado, foi pedido que eu requisitasse os seguintes dados em formulário
    . quantidade de ações 
    . preço unitário da ação
    . corretagem
5. Dos itens mencionados em "4", dê um valor para cada um e faça os cálculos pedidos nos pontos
*/

const range = (min, max) => {
  return Array.from({length: max - min + 1}, (value, key) => key + min)
}

const has_proper_values = range(0, 9)
// console.log(has_proper_values)
const tax = '100.2'
// console.log(Number(tax[0] + tax[1]) <= 99)

console.log(what_day_is_today())
