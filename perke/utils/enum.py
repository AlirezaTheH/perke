import re
from typing import Tuple

from perke.utils.decorators import classproperty


class Enum:
    """
    Represents an enum with an enums property.
    """

    @classproperty
    def enums(cls) -> Tuple[str, ...]:
        """
        A property to get all enum values.

        Returns
        -------
        result: `tuple[str]`
            Enum values
        """
        return tuple(var for var in vars(cls)
                     if re.search(r'^(_|enums)', var) is None)
