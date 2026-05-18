from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PetForm
from .models import Pet


def listar_gatos(request):
    gatos = Pet.objects.filter(status='disponivel').values(
        'id', 'idade', 'sexo', 'cor', 'descricao', 'foto'
    )
    return JsonResponse(list(gatos), safe=False)


def serve_html_page(request, filename):
    allowed_pages = {
        'index.html',
        'animais.html',
        'como-adotar.html',
        'contato.html',
        'quero-ajudar.html',
    }
    if filename not in allowed_pages:
        raise Http404()

    page_path = settings.BASE_DIR / filename
    if not page_path.exists():
        page_path = settings.BASE_DIR.parent / filename
    if not page_path.exists():
        raise Http404()

    return FileResponse(open(page_path, 'rb'), content_type='text/html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('gatos:dashboard')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('gatos:dashboard')

    return render(request, 'gatos/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('gatos:login')


@login_required
def dashboard(request):
    pets = Pet.objects.all().order_by('-data_entrada')
    return render(request, 'gatos/dashboard.html', {'pets': pets})


@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.usuario_cadastro = request.user
            pet.save()
            messages.success(request, 'Pet cadastrado com sucesso.')
            return redirect('gatos:dashboard')
    else:
        form = PetForm()

    return render(request, 'gatos/pet_form.html', {'form': form, 'titulo': 'Cadastrar novo pet'})


@login_required
def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do pet atualizados com sucesso.')
            return redirect('gatos:dashboard')
    else:
        form = PetForm(instance=pet)

    return render(request, 'gatos/pet_form.html', {'form': form, 'titulo': 'Editar pet'})


@login_required
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, 'Pet excluído com sucesso.')
        return redirect('gatos:dashboard')

    return render(request, 'gatos/pet_delete.html', {'pet': pet})