from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.produtos.views import ProdutoViewSet, CategoriaViewSet
from apps.financeiro.views import CaixaViewSet


routers = DefaultRouter()

routers.register(r'produtos', ProdutoViewSet, basename='produtos')
routers.register(r'categorias', CategoriaViewSet, basename='categorias')
routers.register(r'financeiro/caixas', CaixaViewSet, basename='caixas')

urlpatterns = [
    path('api/', include(routers.urls), name='api'),
]
