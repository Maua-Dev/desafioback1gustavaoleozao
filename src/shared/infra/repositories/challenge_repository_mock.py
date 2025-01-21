from typing import List

from src.shared.domain.entities.challenge import Challenge
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.challenge_repository_interface import IChallengeRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class ChallengeRepositoryMock(IChallengeRepository):
    pass
