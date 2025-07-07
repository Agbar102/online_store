from django.urls import path, include

from .views import UserOrderListView, CheckoutView, SingleProductOrderView


urlpatterns = [
    path('instant/',SingleProductOrderView.as_view(), name='single-product-order'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders-user/', UserOrderListView.as_view(), name='get-order')
]