from dataclasses import dataclass

from django.db.models import Count, Sum

from mining.models import MiningAction

__all__ = (
    'ResourceStatistics',
    'MiningStatistics',
    'get_mining_statistics',
)


@dataclass(frozen=True, slots=True)
class ResourceStatistics:
    name: str
    total_value: int
    total_count: int


@dataclass(frozen=True, slots=True)
class MiningStatistics:
    user_id: int
    resources: list[ResourceStatistics]


def get_mining_statistics(*, user_id: int) -> MiningStatistics:
    resources_statistics = (
        MiningAction.objects
        .filter(user_id=user_id)
        .values('resource_name')
        .annotate(total_value=Sum('value'), total_count=Count('id'))
        .order_by('-total_value')
    )
    return MiningStatistics(
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
