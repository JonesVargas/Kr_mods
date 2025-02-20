from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('mods/', mod_list, name='mod_list'),
    path('download/<int:mod_id>/', download_mod, name='download_mod'),
    path('comment/<int:mod_id>/', add_comment, name='add_comment'),
    path('sugerir/', sugerir, name='sugerir'),  
    path('sugerir/like/<int:sugestao_id>/', like_sugestao, name='like_sugestao'),  
    path('sugerir/dislike/<int:sugestao_id>/', dislike_sugestao, name='dislike_sugestao'),
    path('login/', login_view, name='login'),  # Usando a nova função de login
    path('register/', register, name='register'),
    path('purchase/<int:mod_id>/', purchase_mod, name='purchase_mod'),
    path('my-mods/', user_purchases, name='user_purchases'),
]
