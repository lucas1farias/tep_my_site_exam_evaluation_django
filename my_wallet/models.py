

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class Base(models.Model):
    created = models.DateTimeField('Data de criação', auto_now_add=True)
    updated = models.DateTimeField('Última atualização', auto_now=True)
    availability = models.BooleanField('Disponibilidade', default=True)

    class Meta:
        abstract = True


class Investor(Base):
    PROFILE_CHOICES = (
        ('c', 'conservador'),
        ('m', 'moderado'),
        ('a', 'arrojado')
    )

    profile = models.CharField('Perfil de risco', max_length=1, choices=PROFILE_CHOICES)
    investor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investor')

    def __str__(self):
        return self.investor.username

    class Meta:
        verbose_name = 'Investidor'
        verbose_name_plural = 'Investidores'


class Stock(Base):
    code = models.CharField('Código', max_length=6)
    company_name = models.CharField('Nome da empresa', max_length=150)
    corporate_taxpayer_registry = models.CharField('CNPJ da empresa', max_length=18)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def stock_code_is_valid(self, stock_size, target, alternative):
        alphabet = [letter.upper() for letter in 'a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r.s.t.u.v.w.x.y.z'.split('.')]
        numbers = [str(n) for n in range(10)]
        proper_stock_sizes = (5, 6)

        stock_code = ''
        if not alternative:
            stock_code = str(self.code)
        else:
            stock_code = target

        stock_has_proper_size = stock_size in proper_stock_sizes
        first_four_must_be_letters = stock_code[0] in alphabet and \
            stock_code[1] in alphabet and \
            stock_code[2] in alphabet and \
            stock_code[3] in alphabet
        length_five_last_one_is_number = (len(stock_code) - 1) == 5 and stock_code[-1] in numbers
        length_six_last_two_ones_are_number = (len(stock_code) - 1) == 6 and stock_code[-1] in numbers and stock_code[-2] in numbers

        requirements = None
        validation = []

        if stock_size == 5:
            requirements = (
                stock_has_proper_size,
                first_four_must_be_letters,
                length_five_last_one_is_number,
            )
        elif stock_size == 6:
            requirements = (
                stock_has_proper_size,
                first_four_must_be_letters,
                length_six_last_two_ones_are_number
            )
        else:
            return False

        for requirement in requirements:
            improper = requirement is False
            proper = requirement is True
            if improper:
                validation.append(False)
            if proper:
                pass

        report = len(validation) == 0
        return report

    def cnpj_is_valid(self, target, alternative):
        code = ''

        if not alternative:
            code = str(self.corporate_taxpayer_registry)
        else:
            code = target

        code_has_proper_size = len(code) == 18
        has_first_dot = code[2] == '.'
        has_second_dot = code[6] == '.'
        has_proper_dash = code[10] == '/'
        has_proper_minus = code[15] == '-'
        requirements = (code_has_proper_size, has_first_dot, has_second_dot, has_proper_dash, has_proper_minus)
        validation = []

        for requirement in requirements:
            improper = requirement is False
            proper = requirement is True
            if improper:
                validation.append(False)
            if proper:
                pass

        report = len(validation) == 0
        return report

    def save(self, *args, **kwargs):

        # Validadores que impedem de criar códigos de Stock caso estejam com formatação incorreta
        stock_code_is_valid = self.stock_code_is_valid(
            stock_size=len(str(self.code)) - 1, target=None, alternative=False
        )
        cnpj_is_valid = self.cnpj_is_valid(
            target=None, alternative=False
        )

        if stock_code_is_valid and cnpj_is_valid:
            super().save(*args, **kwargs)


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
    tax = models.DecimalField('Taxa de corretagem', max_digits=6, decimal_places=2)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name='transaction')

    def __str__(self):
        return self.stock.code

    class Meta:
        verbose_name = 'Transações'
        verbose_name_plural = 'Transações'

    def date_validity(self):

        try:
            current_year = datetime.now().year
            one_century_later = current_year + 100
            day_calculus = int(self.creation_date[0] + self.creation_date[1])
            month_calculus = int(self.creation_date[3] + self.creation_date[4])
            year_calculus = int(self.creation_date[6] + self.creation_date[7] + self.creation_date[8] + self.creation_date[9])

            has_proper_size = len(str(self.creation_date)) == 10
            has_proper_day = 0 < day_calculus <= 31
            has_first_dash = self.creation_date[2] == '/'
            has_proper_month = 0 < month_calculus <= 12
            has_second_dash = self.creation_date[5] == '/'
            has_proper_year = current_year <= year_calculus <= one_century_later

            requirements = [has_proper_size, has_proper_day, has_proper_month, has_proper_year, has_first_dash,
                            has_second_dash]

            if False in requirements:
                return False
            return True
        except ValueError:
            return False

    def save(self, *args, **kwargs):
        date_is_proper = self.date_validity()
        if date_is_proper:
            super().save(*args, **kwargs)
