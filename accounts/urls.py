

from django.urls import path
from .views import *

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('criar-conta', SignUpView.as_view(), name='criar-conta'),
    path('iniciar-sessao', SignInView.as_view(), name='iniciar-sessao'),
    path('encerrar-sessao', sign_out, name='encerrar-sessao')
]
