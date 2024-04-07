from django.urls import path

from quizzes.views import (
    RandomPredictionApi, RandomTruthOrDareQuestionApi, RandomWishApi,
)

urlpatterns = [
    path(
        r'wishes/random/',
        RandomWishApi.as_view(),
        name='random-wish-retrieve',
    ),
    path(
        r'predictions/random/',
        RandomPredictionApi.as_view(),
        name='random-prediction-retrieve',
    ),
    path(
        r'truth-or-dare/random/',
        RandomTruthOrDareQuestionApi.as_view(),
        name='random-truth-or-dare-question-retrieve',
    ),
]
