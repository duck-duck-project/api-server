from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quizzes.models import TruthOrDareQuestion
from quizzes.selectors import (
    get_random_prediction_text,
    get_random_truth_or_dare_question,
    get_random_wish_text,
)

__all__ = (
    'RandomWishApi',
    'RandomTruthOrDareQuestionApi',
    'RandomPredictionApi',
)


class RandomPredictionApi(APIView):

    def get(self, request: Request) -> Response:
        prediction = get_random_prediction_text()
        return Response({'text': prediction})


class RandomWishApi(APIView):
    class OutputSerializer(serializers.Serializer):
        text = serializers.CharField()

    def get(self, request: Request) -> Response:
        wish = get_random_wish_text()
        return Response({'text': wish})


class RandomTruthOrDareQuestionApi(APIView):
    class InputSerializer(serializers.Serializer):
        type = serializers.ChoiceField(
            choices=TruthOrDareQuestion.Type.choices,
            default=None,
        )

    class OutputSerializer(serializers.Serializer):
        text = serializers.CharField()
        type = serializers.ChoiceField(choices=TruthOrDareQuestion.Type.choices)

    def get(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        question_type: TruthOrDareQuestion.Type | None = serializer.data['type']

        question = get_random_truth_or_dare_question(
            question_type=question_type,
        )
        serializer = self.OutputSerializer(question)
        return Response(serializer.data)
