from relationships.services.relationships import UserInRelationship

__all__ = ('UserHasNoRelationshipError',)


class UserHasNoRelationshipError(Exception):

    def __init__(self, user_in_relationship: UserInRelationship):
        self.user_in_relationship = user_in_relationship
        super().__init__(
            f'User ID{user_in_relationship.id} has no active relationship',
        )
