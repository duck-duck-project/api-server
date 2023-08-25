from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.exceptions import TeamDoesNotExistError
from users.selectors.teams import (
    get_team_ids_and_names_by_user_id,
    get_team_by_id,
)
from users.services.teams import create_team

__all__ = (
    'TeamListCreateApi',
    'TeamRetrieveApi',
)


class TeamSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField()
    members_count = serializers.IntegerField()


class TeamListCreateApi(APIView):

    class CreateInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=64)

    class ListOutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()

    def get(self, request: Request, user_id: int):
        teams = get_team_ids_and_names_by_user_id(user_id)
        serializer = self.ListOutputSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request: Request, user_id: int):
        serializer = self.CreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        name: str = serialized_data['name']

        team = create_team(name=name, user_id=user_id)
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeamRetrieveApi(APIView):

    def get(self, request: Request, team_id: int):
        try:
            team = get_team_by_id(team_id)
        except TeamDoesNotExistError:
            raise NotFound('Team does not exist')
        serializer = TeamSerializer(team)
        return Response(serializer.data)
