import random

from rest_framework.exceptions import NotFound

from quizzes.models import TruthOrDareQuestion

__all__ = ('get_random_truth_or_dare_question',)


def get_random_truth_or_dare_question(
        *,
        question_type: TruthOrDareQuestion.Type | None = None,
) -> TruthOrDareQuestion:
    questions = TruthOrDareQuestion.objects.all()
    if question_type is not None:
        questions = questions.filter(type=question_type)

    question_ids = questions.values_list('id', flat=True)

    if not question_ids:
        raise NotFound('No questions found')

    try:
        return TruthOrDareQuestion.objects.get(id=random.choice(question_ids))
    except TruthOrDareQuestion.DoesNotExist:
        raise NotFound('No questions found')
