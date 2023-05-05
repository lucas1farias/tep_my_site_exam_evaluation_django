

from django.shortcuts import render
from django.contrib.messages import success
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .models import *
from utils.functions import *


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    # Objetos de stock são criados quando o banco de Stocks estiver vazio
    create_stocks_if_db_is_empty(db=Stock, amount=100)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user.username
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
