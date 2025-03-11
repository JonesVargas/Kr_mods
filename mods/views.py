from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import *
from django.http import FileResponse
from django.contrib import messages
from django.views.decorators.cache import never_cache
import cloudinary.utils


def home(request):
    secoes = HomePageSection.objects.prefetch_related("conteudos").all()
    redes_sociais = RedeSocial.objects.all()

    # Garante que a URL da imagem seja retornada corretamente no template
    for secao in secoes:
        for conteudo in secao.conteudos.all():
            if conteudo.imagem:
                conteudo.imagem_url = conteudo.imagem.url if hasattr(conteudo.imagem, 'url') else ""

    for rede in redes_sociais:
        if rede.icone:
            rede.icone_url = rede.icone.url if hasattr(rede.icone, 'url') else ""

    context = {
        'secoes': secoes,
        'redes_sociais': redes_sociais,
    }

    return render(request, 'mods/home.html', context)


def get_logo(request):
    """Esta função será usada em base.html para garantir que a logo seja carregada dinamicamente."""
    homepage = HomePage.objects.first()
    logo_url = homepage.logo.url if homepage and homepage.logo else ""
    return {'homepage': homepage, 'logo_url': logo_url}


def mod_list(request):
    mods = Mod.objects.prefetch_related('comments').all()

    for mod in mods:
        if mod.image:
            mod.image_url = mod.image.url if hasattr(mod.image, 'url') else ""

    return render(request, 'mods/mod_list.html', {'mods': mods})


@login_required
def download_mod(request, mod_id):
    mod = get_object_or_404(Mod, id=mod_id)

    # Verifica se o mod é pago e se o usuário comprou
    if not mod.is_free() and not Purchase.objects.filter(user=request.user, mod=mod).exists():
        messages.error(request, "Você precisa comprar este mod antes de baixá-lo.")
        return redirect('purchase_mod', mod_id=mod.id)

    return FileResponse(mod.file.open(), as_attachment=True, filename=mod.file.name)


@login_required
def add_comment(request, mod_id):
    mod = get_object_or_404(Mod, id=mod_id)

    if request.method == "POST":
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(user=request.user, mod=mod, text=comment_text)

    return redirect('mod_list')


@never_cache
@login_required
def sugerir(request):
    if request.method == "POST":
        descricao = request.POST.get("descricao")
        if descricao:
            SugestaoMod.objects.create(usuario=request.user, descricao=descricao)
            messages.success(request, "Sugestão enviada com sucesso!")
            return redirect("sugerir")

    sugestoes = SugestaoMod.objects.all().order_by('-criado_em')
    return render(request, 'mods/sugerir.html', {'sugestoes': sugestoes})


@never_cache
def listar_sugestoes(request):
    sugestoes = SugestaoMod.objects.all().order_by('-criado_em')
    return render(request, 'mods/sugerir.html', {'sugestoes': sugestoes})


@login_required
def like_sugestao(request, sugestao_id):
    sugestao = get_object_or_404(SugestaoMod, id=sugestao_id)
    sugestao.likes += 1
    sugestao.save()
    return redirect("sugerir")


@login_required
def dislike_sugestao(request, sugestao_id):
    sugestao = get_object_or_404(SugestaoMod, id=sugestao_id)
    sugestao.dislikes += 1
    sugestao.save()
    return redirect("sugerir")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automático
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'mods/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            users = User.objects.filter(email=email)  # Busca usuários com o e-mail fornecido
            
            if users.exists():  # Se houver algum usuário com esse e-mail
                user = users.first()  # Pega o primeiro usuário encontrado
                
                authenticated_user = authenticate(username=user.username, password=form.cleaned_data.get("password"))

                if authenticated_user:
                    login(request, authenticated_user)
                    return redirect('home')

    else:
        form = EmailLoginForm()

    return render(request, 'mods/login.html', {'form': form})


@login_required
def purchase_mod(request, mod_id):
    mod = get_object_or_404(Mod, id=mod_id)

    if mod.is_free():
        return redirect('download_mod', mod_id=mod.id)  # Redireciona diretamente para download se for grátis

    if request.method == "POST":
        # Verifica se o usuário já comprou esse mod
        if Purchase.objects.filter(user=request.user, mod=mod).exists():
            return redirect('user_purchases')

        # Registra a compra
        Purchase.objects.create(user=request.user, mod=mod)
        return redirect('user_purchases')

    return render(request, 'mods/purchase_confirm.html', {'mod': mod})


@login_required
def user_purchases(request):
    purchases = Purchase.objects.filter(user=request.user)

    return render(request, 'mods/user_purchases.html', {'purchases': purchases})
