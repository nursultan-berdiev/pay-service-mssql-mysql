from django.urls import path
from .views import CheckList, CustomerList, update_customers, PaymentList, make_income_operation
from . import views
from django.conf.urls import url

urlpatterns = [
    path('customers/',CustomerList.as_view(), name='customers'),
    path('update-customers/', update_customers, name='update-customers'),
    path('', PaymentList.as_view(), name='payment'),
    path('customers/pay/<pk>/', make_income_operation, name='make-income-operation'),
    path('check', CheckList.as_view(), name='check'),
]
