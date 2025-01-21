from decimal import Decimal
from typing import List

from src.shared.domain.entities.challenge import Challenge
from src.shared.domain.repositories.challenge_repository_interface import IChallengeRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.dto.challenge_dynamo_dto import ChallengeDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource


class ChallengeRepositoryDynamo(IChallengeRepository):
    pass