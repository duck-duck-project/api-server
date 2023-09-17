from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from economics.services import compute_user_balance
from users.exceptions import UserDoesNotExistsError
from users.selectors.users import get_user_by_id

__all__ = ('BalanceRetrieveApi',)


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
