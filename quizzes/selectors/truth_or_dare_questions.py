import random

from quizzes.exceptions import TruthOrDareQuestionNotFoundError
from quizzes.models import TruthOrDareQuestion

__all__ = ('get_random_truth_or_dare_question',)


def get_random_truth_or_dare_question(
        *,
        question_type: TruthOrDareQuestion.Type | None = None,
) -> TruthOrDareQuestion:
    """
    Get random truth or dare question.

    Keyword Args:
        question_type: truth or dare question type number.

    Returns:
        TruthOrDareQuestion object.
    """
    questions = TruthOrDareQuestion.objects.all()
    if question_type is not None:
        questions = questions.filter(type=question_type)

    question_ids = questions.values_list('id', flat=True)

    if not question_ids:
        raise TruthOrDareQuestionNotFoundError

    try:
        return TruthOrDareQuestion.objects.get(id=random.choice(question_ids))
    except TruthOrDareQuestion.DoesNotExist:
        raise TruthOrDareQuestionNotFoundError
