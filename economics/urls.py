from django.urls import path

from economics.views import (
    TransactionListApi,
    TransferCreateApi,
    BalanceRetrieveApi,
    SystemDepositCreateApi,
    SystemWithdrawalCreateApi,
    RichestUsersStatisticsApi,
)

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
    path(
        r'balance/users/<int:user_id>/',
        BalanceRetrieveApi.as_view(),
        name='balance-retrieve',
    ),
    path(
        r'richest-users-statistics/',
        RichestUsersStatisticsApi.as_view(),
        name='richest-users-statistics',
    ),
    path(
        r'deposit/',
        SystemDepositCreateApi.as_view(),
        name='system-deposit-create',
    ),
    path(
        r'withdraw/',
        SystemWithdrawalCreateApi.as_view(),
        name='system-withdrawal-create',
    ),
]
