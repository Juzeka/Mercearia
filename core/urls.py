from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.produtos.views import ProdutoViewSet, CategoriaViewSet
from apps.financeiro.views import CaixaViewSet, SangriaViewSet


routers = DefaultRouter()

routers.register(r'produtos', ProdutoViewSet, basename='produtos')
routers.register(r'categorias', CategoriaViewSet, basename='categorias')
routers.register(r'financeiro/caixas', CaixaViewSet, basename='caixas')
routers.register(r'financeiro/sangrias', SangriaViewSet, basename='sangrias')

urlpatterns = [
    path('api/', include(routers.urls), name='api'),
]
