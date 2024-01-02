from rest_framework import serializers

from manas_id.models import ManasId, Department

__all__ = ('DepartmentSerializer', 'ManasIdSerializer',)


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class ManasIdSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = ManasId
        fields = (
            'user_id',
            'department',
            'first_name',
            'last_name',
            'born_at',
            'course',
            'gender',
        )