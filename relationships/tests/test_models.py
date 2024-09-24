import pytest

from relationships.models import Relationship


@pytest.mark.parametrize(
    'experience, level',
    [
        (0, 0),
        (300, 8),
        (1000, 9),
        (5000, 12),
        (50000, 15),
    ]
)
def test_relationship_level(experience, level):
    relationship = Relationship(experience=experience)
    assert relationship.level == level


@pytest.mark.parametrize(
    'experience, next_level',
    [
        (0, 1),
        (300, 9),
        (1000, 10),
        (5000, 13),
        (50000, 16),
    ]
)
def test_relationship_next_level(experience, next_level):
    relationship = Relationship(experience=experience)
    assert relationship.next_level == next_level


@pytest.mark.parametrize(
    'experience, next_level_required_experience',
    [
        (0, 2),
        (300, 512),
        (1000, 1024),
        (5000, 8192),
        (50000, 65536),
    ]
)
def test_relationship_next_level_experience(
        experience,
        next_level_required_experience,
):
    relationship = Relationship(experience=experience)
    assert (
            relationship.next_level_required_experience
            == next_level_required_experience
    )


@pytest.mark.parametrize(
    'experience, experience_to_next_level',
    [
        (0, 2),
        (300, 212),
        (1000, 24),
        (5000, 3192),
        (50000, 15536),
    ]
)
def test_relationship_experience_to_next_level(
        experience,
        experience_to_next_level,
):
    relationship = Relationship(experience=experience)
    assert relationship.experience_to_next_level == experience_to_next_level


if __name__ == '__main__':
    pytest.main()
