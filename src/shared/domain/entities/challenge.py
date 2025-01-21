import abc
import re

from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.domain_errors import EntityError


class Challenge(abc.ABC):
    pass
