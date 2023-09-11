from exceptions import ServerAPIError
from models import Transfer
from repositories.base import APIRepository

__all__ = ('TransferRepository',)


class TransferRepository(APIRepository):

    async def create(
            self,
            *,
            sender_id: int,
            recipient_id: int,
            amount: float,
            description: str | None = None,
    ) -> Transfer:
        url = '/economics/transfers/'
        request_data = {
            'sender_id': sender_id,
            'recipient_id': recipient_id,
            'amount': amount,
            'description': description,
        }
        async with self._http_client.post(url, json=request_data) as response:
            if response.status != 201:
                raise ServerAPIError
            response_data = await response.json()
        return Transfer.model_validate(response_data)
