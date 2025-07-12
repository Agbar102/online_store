from django.urls import path
from payments.views import CreateCheckoutSessionView, stripe_webhook

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout'),
    path('stripe/webhook/', stripe_webhook),

]