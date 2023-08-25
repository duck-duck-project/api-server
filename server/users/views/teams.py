from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.exceptions import (
    TeamDoesNotExistError,
    TeamMemberAlreadyExistsError, TeamMemberDoesNotExistError
)
from users.models import TeamMember
from users.selectors.teams import (
    get_team_ids_and_names_by_user_id,
    get_team_by_id, get_team_members_by_team_id,
)
from users.services.teams import (
    create_team, delete_team_by_id,
    create_team_member, delete_team_member_by_id
)

__all__ = (
    'TeamListCreateApi',
    'TeamRetrieveDeleteApi',
    'TeamMemberListCreateApi',
    'TeamMemberRetrieveDeleteApi',
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


class TeamRetrieveDeleteApi(APIView):

    def get(self, request: Request, team_id: int):
        try:
            team = get_team_by_id(team_id)
        except TeamDoesNotExistError:
            raise NotFound('Team does not exist')
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    def delete(self, request: Request, team_id: int):
        try:
            delete_team_by_id(team_id)
        except TeamDoesNotExistError:
            raise NotFound('Team does not exist')
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamMemberListCreateApi(APIView):

    class CreateInputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()

    class ListOutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        user_id = serializers.IntegerField()
        user_fullname = serializers.CharField(source='user__fullname')
        user_username = serializers.CharField(
            allow_null=True,
            source='user__username',
        )
        status = serializers.ChoiceField(choices=TeamMember.Status.choices)

    class CreateOutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        user_id = serializers.IntegerField(source='user.id')
        user_fullname = serializers.CharField(source='user.fullname')
        user_username = serializers.CharField(
            allow_null=True,
            source='user.username',
        )
        status = serializers.ChoiceField(choices=TeamMember.Status.choices)
        created_at = serializers.DateTimeField()
        is_hidden = serializers.BooleanField()

    def get(self, request: Request, team_id: int):
        team_members = get_team_members_by_team_id(team_id)
        serializer = self.ListOutputSerializer(team_members, many=True)
        return Response(serializer.data)

    def post(self, request: Request, team_id: int):
        serializer = self.CreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']

        try:
            team_member = create_team_member(team_id=team_id, user_id=user_id)
        except TeamMemberAlreadyExistsError:
            error = APIException('Team member already exists')
            error.status_code = status.HTTP_409_CONFLICT
            raise error

        serializer = self.CreateOutputSerializer(team_member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeamMemberRetrieveDeleteApi(APIView):

    def delete(self, request: Request, team_member_id: int):
        try:
            delete_team_member_by_id(team_member_id)
        except TeamMemberDoesNotExistError:
            raise NotFound('Team member does not exist')
        return Response(status=status.HTTP_204_NO_CONTENT)
