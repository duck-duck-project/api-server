from dataclasses import dataclass

from django.db.models import Count, Sum

from mining.models import MiningAction

__all__ = (
    'ResourceStatistics',
    'MiningUserStatistics',
    'get_mining_user_statistics',
    'get_mining_chat_statistics',
    'MiningChatStatistics',
)


@dataclass(frozen=True, slots=True)
class ResourceStatistics:
    name: str
    total_value: int
    total_count: int


@dataclass(frozen=True, slots=True)
class MiningUserStatistics:
    user_id: int
    resources: list[ResourceStatistics]


@dataclass(frozen=True, slots=True)
class MiningChatStatistics:
    chat_id: int
    resources: list[ResourceStatistics]


def get_mining_user_statistics(*, user_id: int) -> MiningUserStatistics:
    resources_statistics = (
        MiningAction.objects
        .filter(user_id=user_id)
        .values('resource_name')
        .annotate(total_value=Sum('value'), total_count=Count('id'))
        .order_by('-total_value')
    )
    return MiningUserStatistics(
        user_id=user_id,
        resources=[
            ResourceStatistics(
                name=resource['resource_name'],
                total_value=resource['total_value'],
                total_count=resource['total_count'],
            )
            for resource in resources_statistics
        ]
    )


def get_mining_chat_statistics(*, chat_id: int) -> MiningChatStatistics:
    resources_statistics = (
        MiningAction.objects
        .filter(chat_id=chat_id)
        .values('resource_name')
        .annotate(total_value=Sum('value'), total_count=Count('id'))
        .order_by('-total_value')
    )
    return MiningChatStatistics(
        chat_id=chat_id,
        resources=[
            ResourceStatistics(
                name=resource['resource_name'],
                total_value=resource['total_value'],
                total_count=resource['total_count'],
            )
            for resource in resources_statistics
        ]
    )
