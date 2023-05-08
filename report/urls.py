

from django.urls import path
from .views import *

urlpatterns = [
    path('relatorio', index, name='relatorio')
]
