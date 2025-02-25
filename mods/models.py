from django.db import models
from django.contrib.auth.models import User

class Mod(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='mods/')
    image = models.ImageField(upload_to='mods/images/', null=True, blank=True)  # Imagem opcional
    youtube_link = models.URLField(null=True, blank=True)  # Link opcional
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 0 = grátis
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Mantemos User padrão
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.user.username


class HomePage(models.Model):
    logo = models.ImageField(upload_to='homepage/', null=True, blank=True)  # Logo do site
    apresentacao_texto = models.TextField()  # Texto de apresentação

    def __str__(self):
        return "Configuração da Página Inicial"


class ApresentacaoImagem(models.Model):
    homepage = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="apresentacao_imagens")
    imagem = models.ImageField(upload_to='homepage/imagens/')
    descricao = models.TextField()

    def __str__(self):
        return self.descricao[:50]  # Mostra apenas os primeiros 50 caracteres


class Noticia(models.Model):
    homepage = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="noticias")
    titulo = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='homepage/noticias/', null=True, blank=True)
    video = models.URLField(null=True, blank=True)  # Link para vídeo opcional (YouTube, etc.)
    descricao = models.TextField()

    def __str__(self):
        return self.titulo


class HomePageSection(models.Model):
    """Modelo que representa uma seção da homepage."""
    titulo = models.CharField(max_length=255)
    ordem = models.PositiveIntegerField(default=0)  # Para definir a ordem das seções

    class Meta:
        ordering = ['ordem']
        verbose_name = "Seção da Página Inicial"
        verbose_name_plural = "Seções da Página Inicial"

    def __str__(self):
        return self.titulo


class SectionContent(models.Model):
    """Conteúdo dentro de uma seção da homepage (imagem/vídeo + título + descrição)."""
    section = models.ForeignKey(HomePageSection, on_delete=models.CASCADE, related_name="conteudos")
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='homepage/conteudos/', null=True, blank=True)
    video = models.URLField(null=True, blank=True)  # Link do vídeo (YouTube, etc.)
    ordem = models.PositiveIntegerField(default=0)  # Para definir a ordem dos itens dentro da seção

    class Meta:
        ordering = ['ordem']  # Os conteúdos aparecem na ordem definida pelo admin
        verbose_name = "Conteúdo da Seção"
        verbose_name_plural = "Conteúdos das Seções"

    def __str__(self):
        return self.titulo
    
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    mod = models.ForeignKey(Mod, on_delete=models.CASCADE, related_name="purchases")
    purchased_at = models.DateTimeField(auto_now_add=True)  # Data da compra

    class Meta:
        unique_together = ('user', 'mod')  # Evita compras duplicadas

    def __str__(self):
        return f"{self.user.username} comprou {self.mod.title}"


class SugestaoMod(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona a sugestão ao usuário que a criou
    descricao = models.TextField()  # Texto da sugestão
    likes = models.PositiveIntegerField(default=0)  # Contador de curtidas
    dislikes = models.PositiveIntegerField(default=0)  # Contador de descurtidas
    criado_em = models.DateTimeField(auto_now_add=True)  # Data de criação da sugestão

    def __str__(self):
        return f"{self.usuario.username} - {self.descricao[:30]}"
    

class RedeSocial(models.Model):
    nome = models.CharField(max_length=50, unique=True)  # Nome da rede (Ex: Instagram, Facebook)
    icone = models.ImageField(upload_to="redes_sociais/")  # Upload do ícone
    link = models.URLField()  # URL para a rede social

    def __str__(self):
        return self.nome


