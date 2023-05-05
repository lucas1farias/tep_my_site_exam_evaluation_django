

from random import choice
from datetime import datetime


def create_object(label, db, fields):
    if label == 'user':
        return db.objects.create_user(username=fields[0], email=fields[1], password=fields[2])
    elif label == 'investor':
        return db(profile=fields[0], investor=fields[1])
    elif label == 'transaction':
        return db(
            creation_date=fields[0],
            stock=fields[1],
            stock_shares=fields[2],
            share_unit_price=fields[3],
            operation=fields[4],
            tax=fields[5],
            investor=fields[6]
        )


def call_model(model):
    return model.objects.all()


# Funções criadas p/ criar 100 objetos de ação SE: o modelo "Stock" não tiver objetos
def create_stocks_code(amount):
    # Símbolos usados na criação de uma ação (4 letras & 1 número) (4 letras e 2 números)
    alphabet = [letter.upper() for letter in 'a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r.s.t.u.v.w.x.y.z'.split('.')]
    numbers = [str(n) for n in range(10)]

    # Onde os grupos de ações são inseridos
    stocks_set = set({})

    while len(stocks_set) < amount:
        stock_choices = [str(id_) for id_ in tuple(range(1, 3))]
        stock_numbers = choice(stock_choices)
        four_letters = choice(alphabet) + choice(alphabet) + choice(alphabet) + choice(alphabet)
        stock_number_official = 0

        if stock_numbers == '1':
            stock_number_official = choice(numbers)
        elif stock_numbers == '2':
            stock_number_official = choice(numbers) + choice(numbers)

        stock_generated = four_letters + stock_number_official
        stocks_set.add(stock_generated)

    return tuple(stocks_set)


def create_company_name(amount):
    vowels = 'a.e.i.o.u'.split('.')
    consonants = 'b.br.c.cr.d.dr.f.fr.g.gr.nh.j.l.m.n.p.pr.r.s.t.tr.v'.split('.')

    companies_box = set({})
    company_name = ''
    starts_with = tuple(range(2))
    middle_content = tuple(range(2))

    while len(companies_box) < amount:
        if choice(starts_with) == 0:
            company_name = choice(vowels) + choice(consonants) + choice(consonants)  # Ex: Abr
        elif choice(starts_with) == 1:
            company_name = choice(consonants) + choice(vowels) + choice(vowels)      # Ex: Bai
        if choice(middle_content) == 0:
            company_name += choice(vowels) + choice(vowels)                          # Ex: Abreu
        elif choice(middle_content) == 1:
            company_name += choice(consonants) + choice(vowels)                      # Baina

        company_name += choice(consonants) + choice(vowels)                          # Ex: Abreuvo / Bainava
        label = company_name
        vowel_amount = label.count('a') + label.count('e') + label.count('i') + label.count('o') + label.count('u')

        if len(company_name) == 7 and vowel_amount == 4:

            company_name = company_name.title()
            companies_box.add(company_name)
            company_name = ''

    return tuple(companies_box)


def create_cnpj(amount):
    from random import choice

    numbers = tuple(range(10))
    cnpj_box = set({})

    while len(cnpj_box) < amount:
        two = f'{choice(numbers)}{choice(numbers)}'
        two_again = f'{choice(numbers)}{choice(numbers)}'
        three = f'{choice(numbers)}{choice(numbers)}{choice(numbers)}'
        three_again = f'{choice(numbers)}{choice(numbers)}{choice(numbers)}'
        four = f'{choice(numbers)}{choice(numbers)}{choice(numbers)}{choice(numbers)}'
        code = f'{two}.{three}.{three_again}/{four}-{two_again}'
        cnpj_box.add(code)

    return tuple(cnpj_box)


def create_stocks_if_db_is_empty(db, amount):
    if len(db.objects.all()) == 0:
        box_of_stocks = create_stocks_code(amount=amount)
        box_of_companies = create_company_name(amount=amount)
        box_of_cnpj = create_cnpj(amount)

        for i, index in enumerate(box_of_stocks):
            new_stock = db(
                code=box_of_stocks[i],
                company_name=box_of_companies[i],
                corporate_taxpayer_registry=box_of_cnpj[i]
            )
            new_stock.save()


def date_validity(target_date):

    try:
        current_year = datetime.now().year
        one_century_later = current_year + 100
        day_calculus = int(target_date[0] + target_date[1])
        month_calculus = int(target_date[3] + target_date[4])
        year_calculus = int(target_date[6] + target_date[7] + target_date[8] + target_date[9])

        has_proper_size = len(target_date) == 10
        has_proper_day = 0 < day_calculus <= 31
        has_first_dash = target_date[2] == '/'
        has_proper_month = 0 < month_calculus <= 12
        has_second_dash = target_date[5] == '/'
        has_proper_year = current_year <= year_calculus <= one_century_later

        requirements = [has_proper_size, has_proper_day, has_proper_month, has_proper_year, has_first_dash, has_second_dash]

        if False in requirements:
            return False
        return True
    except ValueError:
        return False


def treat_floating_number(number):
    number_draft = str(number)
    number_shaped = number_draft.replace(',', '.')
    return float(number_shaped)


def calculate_purchase_value(amount, unit_price):
    amount_ = float(amount)
    unit_price_ = float(unit_price)
    return f'{amount_ * unit_price_:.2f}'


def calculate_overall_taxes(brokerage, purchase_value):
    """
    * brokrage = custo da corretagem
    * Há 3 taxas B3 comuns cobradas
    * (Taxa de negociação, 0,0370%) (taxa de liquidação, 0,0275%) (taxa de registro, 0,0695%), que somadas = 0,1340%
    * A porcentagem das 3 é usada p/ obter a taxa adicional vinda do valor da compra
    * Então seria (B) = 0.1340 * valor da compra
    * E para a taxa total: brokerage + B

    Taxas B3 (B): 0,0325% * V = 0,000325 * R$ 5.000,00 = R$ 1,625
    Taxas totais (T): C + B = R$ 10,00 + R$ 1,625 = R$ 11,625
    """
    brokerage_data = float(brokerage)
    purchase_value_data = float(purchase_value)
    taxes_percentage = 0.1340
    partial_taxes = taxes_percentage * purchase_value_data
    print(partial_taxes)
    total_taxes = brokerage_data + partial_taxes
    return f'{total_taxes:.2f}'


def calculate_trade_value(operation, purchase_value, tax):
    purchase_value_data = float(purchase_value)
    tax_data = float(tax)

    if operation == 'compra':
        return f'{purchase_value_data + tax_data:.2f}'
    else:
        return f'{purchase_value_data - tax_data:.2f}'


# print(create_stocks_code(100))
# print(create_cnpj(100))
# print(create_company_name(100))
print(create_cnpj(1))
