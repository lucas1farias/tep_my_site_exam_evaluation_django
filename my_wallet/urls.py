

from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('nova-transacao', NewTransactionView.as_view(), name='nova-transacao'),
    path('transacoes-usuario', TransactionsView.as_view(), name='transacoes-usuario'),
    path('editar-transacao/<int:pk>', TransactionAnyField.as_view(), name='editar-transacao'),
    path('remover-transacao/<int:pk>', TransactionDelete.as_view(), name='remover-transacao'),
    path('detalhe-transacao/<int:pk>', TransactionCalculus.as_view(), name='detalhe-transacao'),
    # path('searched-stock', searched_stock, name='searched-stock'),
]
