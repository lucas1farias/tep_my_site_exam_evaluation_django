

def pendencias():
    """
    * Tentar adicionar um perfil com os dados da conta logada (botão "Ver perfil")
    * Tentar criar uma validador para a taxa de corretagem no template "new_transaction.html"
    * Tentar melhorar o validador de data no template "new_transaction"
    * Tentar achar uma maneira mais fácil de fazer modelos acessarem atributos de seus pares
    * Tentar criar um botão de voltar mais real (https://www.youtube.com/watch?v=_P-guJX-TtU&t=720s)

    ========== SOLUÇÃO ATUAL =========
    # Tentativa de avisar no template quando o usuário logado não possuir transação
        for t in context['active_user_transactions']:
            user_id = t.__dict__['investor_id']
            username = str(Investor.objects.get(pk=user_id))
            if username == context['active_user']:
                context['active_user_has_transactions'] = True
                break
        return context
    """


def contexto():
    """
    In Django, when there is a relationship between models, how can I access attributes from the father models through
    the child model in Django without doing complex iterations?

    In Django, you can access attributes from the parent model through the child model using the related name of the
    field that represents the relationship between them.

    * ========== models.py ==========
    class Author(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField()

    class Book(models.Model):
        title = models.CharField(max_length=200)
        author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
        published_date = models.DateField()

    EXISTE UMA GRANDE CHANCE DE "related_name" SE TORNAR UMA FUNÇÃO USÁVEL NO MODELO FILHO (var: books)
    Here, the Book model has a foreign key relationship to the Author model, with the related_name parameter set to
    'books'. This means that for each Author object, you can access a list of all the books they have written by using
     the books attribute, like this:

    * ========== views.py / terminal ==========
    author = Author.objects.get(name='J.K. Rowling')
    books = author.books.all()  # Returns all books written by J.K. Rowling

    In a template, you can access the books attribute using the dot notation:

    * ========== template ==========
    {% for book in author.books.all %}
        <p>{{ book.title }}</p>
    {% endfor %}

    Here, author.books.all returns all books written by the author object.
    """
