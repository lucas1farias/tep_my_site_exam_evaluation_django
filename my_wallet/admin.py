

from django.contrib import admin
from .models import *


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'profile', 'investor'
    )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'code', 'company_name', 'corporate_taxpayer_registry'
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'investor', 'creation_date', 'stock', 'stock_shares', 'share_unit_price', 'operation'
    )
