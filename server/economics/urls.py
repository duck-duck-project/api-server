from django.urls import path

from economics.views import TransactionListApi, TransferCreateApi

app_name = 'economics'
urlpatterns = [
    path(
        r'transactions/users/<int:user_id>/',
        TransactionListApi.as_view(),
        name='transactions-list',
    ),
    path(
        r'transfers/',
        TransferCreateApi.as_view(),
        name='transfers-create',
    ),
]
