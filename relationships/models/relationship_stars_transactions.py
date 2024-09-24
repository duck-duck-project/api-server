from django.db import models

from relationships.models.relationships import Relationship

__all__ = ('RelationshipStarsTransaction',)


class RelationshipStarsTransaction(models.Model):
    relationship = models.ForeignKey(to=Relationship, on_delete=models.CASCADE)
    amount = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=~models.Q(amount__exact=0),
                name='amount_must_not_be_zero',
                violation_error_message='Amount must not be zero.'
            ),
        )
