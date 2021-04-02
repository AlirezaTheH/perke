import re
from typing import Tuple

from decorators import classproperty


class Enum:
    @classproperty
    def enums(cls) -> Tuple[str]:
        return tuple(var for var in vars(cls)
                     if re.search(r'^(_|enums)', var) is None)
