from django.contrib import admin
from .models import *

# Exibir imagem no Django Admin
from django.utils.html import format_html

class ModAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'mod_image_preview')
    search_fields = ('title',)
    list_filter = ('price',)
    fields = ('title', 'description', 'file', 'image', 'youtube_link', 'price')

    readonly_fields = ('mod_image_preview',)

    def mod_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "Sem imagem"

    mod_image_preview.short_description = "Prévia da Imagem"

class ApresentacaoImagemInline(admin.TabularInline):
    model = ApresentacaoImagem
    extra = 1  # Permite adicionar novas imagens diretamente
    readonly_fields = ('imagem_preview',)

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.imagem.url)
        return "Sem imagem"

    imagem_preview.short_description = "Prévia da Imagem"

class NoticiaInline(admin.TabularInline):
    model = Noticia
    extra = 1  # Permite adicionar notícias diretamente
    readonly_fields = ('noticia_imagem_preview',)

    def noticia_imagem_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.imagem.url)
        return "Sem imagem"

    noticia_imagem_preview.short_description = "Prévia da Imagem"

class HomePageAdmin(admin.ModelAdmin):
    inlines = [ApresentacaoImagemInline, NoticiaInline]
    list_display = ('homepage_logo_preview',)

    readonly_fields = ('homepage_logo_preview',)

    def homepage_logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.logo.url)
        return "Sem imagem"

    homepage_logo_preview.short_description = "Prévia do Logo"

class SectionContentInline(admin.TabularInline):
    model = SectionContent
    extra = 1  # Permite adicionar novos conteúdos diretamente
    readonly_fields = ('section_content_preview',)

    def section_content_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.imagem.url)
        return "Sem imagem"

    section_content_preview.short_description = "Prévia da Imagem"

class HomePageSectionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ordem')
    ordering = ['ordem']
    inlines = [SectionContentInline]  # Adiciona os conteúdos diretamente na seção

@admin.register(SugestaoMod)
class SugestaoModAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'descricao', 'likes', 'dislikes', 'criado_em')
    search_fields = ('descricao', 'usuario__username')
    list_filter = ('criado_em',)

@admin.register(RedeSocial)
class RedeSocialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'link', 'rede_social_preview')  # Exibir nome, link e imagem no Django Admin
    readonly_fields = ('rede_social_preview',)

    def rede_social_preview(self, obj):
        if obj.icone:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.icone.url)
        return "Sem imagem"

    rede_social_preview.short_description = "Ícone"

admin.site.register(HomePageSection, HomePageSectionAdmin)
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(Mod, ModAdmin)
admin.site.register(Comment)
