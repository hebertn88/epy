from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('altera_senha/<int:id>', views.altera_senha, name='altera_senha'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]