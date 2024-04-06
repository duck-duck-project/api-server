from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from economics.services import (
    compute_user_balance,
    get_user_balances,
    sort_richest_users,
)
from users.exceptions import UserDoesNotExistsError
from users.selectors.users import get_user_by_id

__all__ = (
    'BalanceRetrieveApi',
    'RichestUsersStatisticsApi',
    'RichestUsersStatisticsView',
)


class BalanceRetrieveApi(APIView):

    def get(self, request: Request, user_id: int):
        try:
            user = get_user_by_id(user_id)
        except UserDoesNotExistsError:
            raise NotFound('User does not exists')
        balance = compute_user_balance(user)
        response_data = {
            'user_id': user.id,
            'balance': balance,
        }
        return Response(response_data)


class RichestUsersStatisticsApi(APIView):

    class InputSerializer(serializers.Serializer):
        limit = serializers.IntegerField(default=10)

    class OutputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        user_fullname = serializers.CharField()
        user_username = serializers.CharField(allow_null=True)
        balance = serializers.IntegerField()

    def get(self, request: Request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        limit: int = serialized_data['limit']

        user_balances = get_user_balances()
        richest_users_top = sort_richest_users(user_balances)

        richest_users = richest_users_top[:limit]

        serialized_users = self.OutputSerializer(richest_users, many=True)
        response_data = {'ok': True, 'result': serialized_users.data}
        return Response(response_data)


class RichestUsersStatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_extensions/richest_users.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user_balances = get_user_balances()
        richest_users = sort_richest_users(user_balances)
        first_50_richest_users = richest_users[:50]
        total_balance = sum(
            user_balance.balance
            for user_balance in first_50_richest_users
        )
        context_data['user_balances'] = first_50_richest_users
        context_data['total_balance'] = total_balance
        return context_data
