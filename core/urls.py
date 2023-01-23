from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.produtos.views import ProdutoViewSet, CategoriaViewSet
from apps.financeiro.views import CaixaViewSet, SangriaViewSet, VendaViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


routers = DefaultRouter()

routers.register(r'produtos', ProdutoViewSet, basename='produtos')
routers.register(r'categorias', CategoriaViewSet, basename='categorias')
routers.register(r'financeiro/caixas', CaixaViewSet, basename='caixas')
routers.register(r'financeiro/sangrias', SangriaViewSet, basename='sangrias')
routers.register(r'financeiro/vendas', VendaViewSet, basename='vendas')

urlpatterns = [
    path('api/', include(routers.urls), name='api'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('doc/api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
