from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .forms import AdotanteForm

def cadastrar_adotante(request):
    if request.method == 'POST':
        form = AdotanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sucesso') # Redireciona após salvar
    else:
        form = AdotanteForm()
    
    return render(request, 'cadastro_adotante.html', {'form': form})