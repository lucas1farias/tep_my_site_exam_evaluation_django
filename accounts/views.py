

from django.views.generic import CreateView, TemplateView

# SignUp
from django.contrib.messages import error, success
from django.shortcuts import redirect
from django.contrib.auth.models import User

# SignIn
from django.contrib.auth import authenticate
from django.contrib.auth import login

# SignOut
from django.contrib.auth import logout

from utils.functions import create_object
from my_wallet.models import Investor  # Importação de um app p/ outro


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_absent'] = self.request.user.is_anonymous
        context['user'] = self.request.user.username
        return context


class SignUpView(CreateView):
    template_name = 'sign_up.html'
    model = User
    fields = ('username', 'email', 'password')

    def post(self, request):
        msg = {
            'username_already_taken': 'O nome de usuário já existe.',
            'user_email_already_taken': 'Já há uma conta registrada com esse e-mail.',
            'passwords_do_not_match': 'Senha inicial e de confirmação, não são idênticas!',
            'sign-up-successful': 'Seu cadastro foi realizado, {account_}!'
        }

        conditions = {
            'passwords_!=': str(request.POST['password']) != str(request.POST['password_confirm']),
            'username_taken': SignUpView.model.objects.filter(username=request.POST['username']).exists(),
            'email_taken': SignUpView.model.objects.filter(email=request.POST['email']).exists()
        }

        # Se estiver enviando dados
        if str(request.method) == 'POST':

            # Senhas ==
            if conditions['passwords_!=']:
                error(request, msg['passwords_do_not_match'])
                return redirect('criar-conta')

            # Usuário já existe
            if conditions['username_taken']:
                error(request, msg['username_already_taken'])
                return redirect('criar-conta')

            # Email já existe
            if conditions['email_taken']:
                error(request, msg['user_email_already_taken'])
                return redirect('criar-conta')

            # Tudo ok
            data_is_proper = True not in tuple(conditions.values())

            if data_is_proper:
                new_user = create_object(
                    label='user',
                    db=SignUpView.model,
                    fields=(request.POST['username'], request.POST['email'], request.POST['password'])
                )

                # O objeto "User" criado acima é passado inteiro como parâmetro para o objeto "Investor"
                # Isso acontece, pois o atributo "investor" do modelo "Investor" é um instância de "User"
                new_investor = create_object(
                    label='investidor',
                    db=Investor,
                    fields=(request.POST['profile'], new_user)
                )

                new_user.save()
                new_investor.save()

                success(request, msg['sign-up-successful'].format(account_=new_user.username))
                return redirect('dashboard')


def sign_out(request):
    user_out = request.user.username
    success(request, f'O usuário {user_out} efetuou sua saída com sucesso!')
    logout(request)
    return redirect('dashboard')


class SignInView(TemplateView):
    template_name = 'sign_in.html'

    def post(self, request):
        msg = {
            'logged_in': 'Login efetuado com sucesso! Olá, {person}',
            'incorrect_data': 'Usuário ou senha incorretas'
        }

        if str(request.method) == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Retorno: True ou None
            user_by_username = authenticate(request, username=username, password=password)

            if user_by_username:
                login(request, user_by_username)
                success(request, msg['logged_in'].format(person=user_by_username))
                return redirect('dashboard')

            else:
                error(request, msg['incorrect_data'])
                return redirect('iniciar-sessao')
