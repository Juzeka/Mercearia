from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.produtos.views import ProdutoViewSet, CategoriaViewSet


routers = SimpleRouter()

routers.register(r'produtos', ProdutoViewSet, basename='produtos')
routers.register(r'produtos/categorias', CategoriaViewSet, basename='categorias')

urlpatterns = [
    path('api/', include(routers.urls), name='api'),
]
