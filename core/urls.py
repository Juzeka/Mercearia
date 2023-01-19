from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.produtos.views import ProdutoViewSet


routers = SimpleRouter()

routers.register(r'produtos', ProdutoViewSet, basename='produtos')

urlpatterns = [
    path('api/', include(routers.urls), name='api'),
]
