

from django.shortcuts import render
from django.contrib.messages import success
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .models import *
from utils.functions import *

from random import randint


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    # Objetos de stock são criados quando o banco de Stocks estiver vazio
    # create_stocks_if_db_is_empty(db=Stock, amount=100)

    # ================================= Formulário p/ crair ativos na página principal =================================
    def post(self, request):
        person_selected_yes_dropdown = self.request.POST.get('new_stocks') == 's'

        # Quando a pessoa clica no botão de criar ativos
        if person_selected_yes_dropdown:
            # Os objetos serão criados parcialmente e verificados abaixo
            amount = (randint(10, 20))
            box_of_stocks = create_stocks_code(amount=amount)
            box_of_companies = create_company_name(amount=amount)
            box_of_cnpj = create_cnpj(amount)

            # Lógica p/ verificar se os ativos criados randomicamente acima já existem no banco
            db_stock = Stock.objects.all()
            each_stock = [i for i in db_stock]
            each_stock_code = [i.__dict__['code'] for i in each_stock]
            each_stock_company_name = [i.__dict__['company_name'] for i in each_stock]
            each_stock_cnpj = [i.__dict__['corporate_taxpayer_registry'] for i in each_stock]

            for i, index in enumerate(box_of_stocks):
                new_stock = Stock(
                    code=box_of_stocks[i],
                    company_name=box_of_companies[i],
                    corporate_taxpayer_registry=box_of_cnpj[i]
                )

                new_stock_name_non_taken = new_stock.code not in each_stock_code
                new_stock_company_name_non_taken = new_stock.code not in each_stock_company_name
                new_stock_cnpj = new_stock.code not in each_stock_cnpj

                # Não achando dados divergentes com os do banco, os objetos novos de ativos podem ser salvos
                if new_stock_name_non_taken and new_stock_company_name_non_taken and new_stock_cnpj:
                    new_stock.save()
            success(request, f'Novos ativos foram add, agora há {get_db_size(Stock)} ativos')

        return redirect('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: Criador de stocks automático
        context['no_stocks'] = check_db_is_empty(Stock)
        context['db_stocks'] = len(call_model(Stock))

        # Os dados do investidor só devem aparecer p/ quem estiver logado
        context['user_absent'] = self.request.user.is_anonymous

        # Tudo isso só pode acontecer se há um usuário cadastrado e logado
        if not context['user_absent']:

            context['user'] = self.request.user.username

            # Todas as transações registradas
            transactions_db = len(call_model(Transaction))

            # Todas as transações do usuário logado
            logged_investor = Investor.objects.get(investor__username=context['user'])
            user_transactions = logged_investor.transaction.all()

            # =============================================== IMPORTANTE ===============================================
            user_stocks_amount = len(user_transactions)

            # =============================================== IMPORTANTE ===============================================
            # Porcentagem de ativos do usuário em relação ao banco de transações
            user_stocks_percentage = get_percentage(reference=user_stocks_amount, main_source=transactions_db, is_float=True)
            user_stocks_percentage_int = get_percentage(reference=user_stocks_amount, main_source=transactions_db, is_float=False)
            # print(user_stocks_percentage)

            # print(context['report'])

            """ alternativo """
            # all_users = tuple((investor.__dict__['investor_id'] for investor in transactions_db))
            # logged_user = tuple((investor.__dict__['investor_id'] for investor in transactions))

            # =============================================== IMPORTANTE ===============================================
            user_stocks_overall_amount = 0
            user_stocks_overall_worth = 0
            user_stocks_overall_amount_operation_purchase = 0
            user_stocks_overall_amount_operation_sale = 0

            for transaction in user_transactions:
                if transaction.operation == 'c':
                    user_stocks_overall_amount_operation_purchase += transaction.stock_shares
                else:
                    user_stocks_overall_amount_operation_sale += transaction.stock_shares

                # print(transaction.stock_shares, transaction.share_unit_price)

                each_stock_total_price = transaction.stock_shares * transaction.share_unit_price

                user_stocks_overall_amount += transaction.stock_shares
                user_stocks_overall_worth += each_stock_total_price

            # print(int(user_stocks_overall_amount))
            # print(float(user_stocks_overall_worth))
            # print(user_stocks_overall_amount_operation_purchase)
            # print(user_stocks_overall_amount_operation_sale)

            context['user_stocks_amount'] = user_stocks_amount
            context['user_stocks_percentage'] = user_stocks_percentage
            context['user_stocks_percentage_int'] = user_stocks_percentage_int
            context['user_stocks_overall_amount'] = user_stocks_overall_amount
            context['user_stocks_overall_worth'] = user_stocks_overall_worth
            context['user_stocks_overall_amount_operation_purchase'] = user_stocks_overall_amount_operation_purchase
            context['user_stocks_overall_amount_operation_sale'] = user_stocks_overall_amount_operation_sale
            return context
        else:
            return context


class NewTransactionView(CreateView):
    template_name = 'new_transaction.html'
    model = Transaction
    fields = ('stock', 'stock_shares', 'share_unit_price', 'operation', 'tax', 'investor')

    def post(self, request):
        if str(request.method) == 'POST':
            stock_input = request.POST.get('stock')
            stock = Stock.objects.get(code=stock_input)

            investor_input = request.POST.get('investor')
            print('===================================================================================================')
            print(investor_input)
            investor = Investor.objects.get(pk=investor_input)
            print('===================================================================================================')
            print(investor)

            # Os campos "stock" e "investor" são relacionados, portanto devem passar o objeto todo
            # Os campos "share_unit_price" e "tax" são decimais, e no template foram convertidos p/ input type="text"
            share_unit_price = treat_floating_number(self.request.POST.get('share_unit_price'))
            tax = treat_floating_number(self.request.POST.get('tax'))

            new_transaction = create_object(
                label='transaction',
                db=NewTransactionView.model,
                fields=(
                    request.POST.get('creation_date'),
                    stock,
                    request.POST.get('stock_shares'),
                    share_unit_price,
                    request.POST.get('operation'),
                    tax,
                    investor
                )
            )
            new_transaction.save()
            success(request, 'Nova transação adicionada!')
            return redirect('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stocks'] = call_model(Stock)
        context['investors'] = call_model(User)
        context['active_user'] = str(self.request.user.username)
        return context


class TransactionsView(ListView):
    template_name = 'transactions.html'
    context_object_name = 'transactions'
    model = Transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_user'] = str(self.request.user.username)
        context['active_user_transactions'] = TransactionsView.model.objects.order_by('created').all()
        # Model.objects.order_by('?').all()
        context['active_user_has_transactions'] = None

        # Tentativa de avisar no template quando o usuário logado não possuir transação
        for t in context['active_user_transactions']:
            user_id = t.__dict__['investor_id']
            username = str(Investor.objects.get(pk=user_id))
            if username == context['active_user']:
                context['active_user_has_transactions'] = True
                break

        return context


class TransactionAnyField(UpdateView):
    template_name = 'transaction_edit.html'
    model = Transaction
    # Campo "investor" foi retirado, pois não é um campo que faz sentido ser editado
    fields = ('stock', 'stock_shares', 'share_unit_price', 'operation', 'tax')
    success_message = 'Informações da transação foram alteradas!'

    def post(self, request, pk, *args, **kwargs):
        if str(self.request.method) == 'POST':

            input_values = {
                'creation_date': request.POST.get('creation_date'),
                'stock': self.request.POST.get('stock'),
                'stock_shares': self.request.POST.get('stock_shares'),
                'share_unit_price': self.request.POST.get('share_unit_price'),
                'operation': self.request.POST.get('operation'),
                'tax': self.request.POST.get('tax')
            }

            # Objeto atual a ser editado
            transaction = TransactionAnyField.model.objects.get(pk=pk)

            if input_values['creation_date']:
                transaction.creation_date = input_values['creation_date']

            # Manter o ativo atual se o usuário não mexer no dropdown do formulário
            if input_values['stock'] == 'unchanged':
                transaction.stock = transaction.stock
            else:
                # Mudar o ativo de acordo com o que for passado no dropdown
                # "stock" anteriormente estava fora do escopo das condições, mas isso estava gerando erro
                # Modificando sua posição p/ cá, resolveu o problema
                stock = Stock.objects.get(code=input_values['stock'])
                transaction.stock = stock

            if input_values['stock_shares'] != '':
                transaction.stock_shares = input_values['stock_shares']

            if input_values['share_unit_price'] != '':
                transaction.share_unit_price = treat_floating_number(input_values['share_unit_price'])

            if input_values['operation'] != '':
                transaction.operation = input_values['operation']

            if input_values['tax'] != '':
                transaction.tax = treat_floating_number(input_values['tax'])

            transaction.save()
            success(request, TransactionAnyField.success_message)
            return redirect('transacoes-usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stocks'] = call_model(Stock)
        return context


class TransactionDelete(DeleteView):
    template_name = 'transaction_delete.html'
    model = Transaction
    success_message = 'Transação removida com êxito!'
    success_url = reverse_lazy('transacoes-usuario')

    def delete(self, request, *args, **kwargs):
        success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class TransactionCalculus(UpdateView):
    template_name = 'details.html'
    model = Transaction
    fields = ('stock', 'stock_shares', 'share_unit_price', 'operation', 'tax')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shares_amount = self.object.stock_shares
        stock_unit_price = self.object.share_unit_price
        context['purchase_value'] = calculate_purchase_value(amount=shares_amount, unit_price=stock_unit_price)
        brokerage = self.object.tax
        context['total_taxes'] = calculate_overall_taxes(brokerage=brokerage, purchase_value=context['purchase_value'])
        operation = self.object.operation
        context['trade_value'] = calculate_trade_value(operation, context['purchase_value'], context['total_taxes'])
        return context


def view_404(request, exception=None):
    return render(request, 'template_404.html', status=404)
