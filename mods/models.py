from django.db import models
from django.contrib.auth.models import User
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Helpers para upload_to (sem pastas)
def mod_image_upload_path(instance, filename):
    return f'mod_{instance.id}_{filename}'

def mod_file_upload_path(instance, filename):
    return f'mod_file_{instance.id}_{filename}'

def homepage_logo_upload_path(instance, filename):
    return f'logo_{filename}'

def apresentacao_imagem_upload_path(instance, filename):
    return f'apresentacao_{instance.id}_{filename}'

def noticia_imagem_upload_path(instance, filename):
    return f'noticia_{instance.id}_{filename}'

def section_content_image_upload_path(instance, filename):
    return f'conteudo_{instance.id}_{filename}'

def rede_social_icone_upload_path(instance, filename):
    return f'icone_{instance.nome}_{filename}'

class Mod(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to=mod_file_upload_path)
    image = models.ImageField(upload_to=mod_image_upload_path, null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_free(self):
        return self.price == 0.00

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mod = models.ForeignKey(Mod, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mod.title} - {self.text[:50]}..."

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.user.username

class HomePage(models.Model):
    logo = models.ImageField(upload_to=homepage_logo_upload_path, null=True, blank=True)
    apresentacao_texto = models.TextField()

    def __str__(self):
        return "Configuração da Página Inicial"

class ApresentacaoImagem(models.Model):
    homepage = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="apresentacao_imagens")
    imagem = models.ImageField(upload_to=apresentacao_imagem_upload_path)
    descricao = models.TextField()

    def __str__(self):
        return self.descricao[:50]

class Noticia(models.Model):
    homepage = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="noticias")
    titulo = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to=noticia_imagem_upload_path, null=True, blank=True)
    video = models.URLField(null=True, blank=True)
    descricao = models.TextField()

    def __str__(self):
        return self.titulo

class HomePageSection(models.Model):
    titulo = models.CharField(max_length=255)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']
        verbose_name = "Seção da Página Inicial"
        verbose_name_plural = "Seções da Página Inicial"

    def __str__(self):
        return self.titulo

class SectionContent(models.Model):
    section = models.ForeignKey(HomePageSection, on_delete=models.CASCADE, related_name="conteudos")
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to=section_content_image_upload_path, null=True, blank=True)
    video = models.URLField(null=True, blank=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']
        verbose_name = "Conteúdo da Seção"
        verbose_name_plural = "Conteúdos das Seções"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        logger.warning(f"DEBUG - Salvando imagem: {self.imagem.name}")
        logger.warning(f"DEBUG - Storage configurado: {settings.DEFAULT_FILE_STORAGE}")
        logger.warning(f"DEBUG - URL após salvar: {self.imagem.url}")

    def __str__(self):
        return self.titulo

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    mod = models.ForeignKey(Mod, on_delete=models.CASCADE, related_name="purchases")
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'mod')

    def __str__(self):
        return f"{self.user.username} comprou {self.mod.title}"

class SugestaoMod(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.descricao[:30]}"

class RedeSocial(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    icone = models.ImageField(upload_to=rede_social_icone_upload_path)
    link = models.URLField()

    def __str__(self):
        return self.nome
