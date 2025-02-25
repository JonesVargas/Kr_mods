from django.contrib import admin
from .models import  *

class ModAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at')
    search_fields = ('title',)
    list_filter = ('price',)
    fields = ('title', 'description', 'file', 'image', 'youtube_link', 'price')

class ApresentacaoImagemInline(admin.TabularInline):
    model = ApresentacaoImagem
    extra = 1  # Permite adicionar novas imagens diretamente

class NoticiaInline(admin.TabularInline):
    model = Noticia
    extra = 1  # Permite adicionar notícias diretamente

class HomePageAdmin(admin.ModelAdmin):
    inlines = [ApresentacaoImagemInline, NoticiaInline]

class SectionContentInline(admin.TabularInline):
    model = SectionContent
    extra = 1  # Permite adicionar novos conteúdos diretamente

class HomePageSectionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ordem')
    ordering = ['ordem']
    inlines = [SectionContentInline]  # Adiciona os conteúdos diretamente na seção

from django.contrib import admin
from .models import SugestaoMod

@admin.register(SugestaoMod)
class SugestaoModAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'descricao', 'likes', 'dislikes', 'criado_em')
    search_fields = ('descricao', 'usuario__username')
    list_filter = ('criado_em',)

@admin.register(RedeSocial)
class RedeSocialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'link')  # Exibir nome e link no Django Admin


admin.site.register(HomePageSection, HomePageSectionAdmin)
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(Mod, ModAdmin)
admin.site.register(Comment)