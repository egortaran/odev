from django.contrib import admin
from django.urls import path, include
from eth_api_app.views import WalletListCreateAPIView, TransactionView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/wallets/', WalletListCreateAPIView.as_view(), name='WalletListCreateAPIView'),
    path('api/v1/transactions/', TransactionView.as_view(), name='TransactionView'),
    path('api-auth/', include('rest_framework.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
