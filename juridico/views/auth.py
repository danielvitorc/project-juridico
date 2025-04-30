from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# ===== Tela de Login ===== 
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirecionar para a página inicial pós-login
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'juridico/login.html')

# ==== Função para deslogar do sistema =====
def logout_usuario(request):
    logout(request)
    return redirect('login')