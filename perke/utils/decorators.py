from typing import Any, Callable


class classproperty:
    """
    A decorator to implement class properties.

    Example
    -------
    .. code:: python

        class Foo:
            @classproperty
            def bar(cls) -> bool:
                return True

        Foo.bar # True

    Attributes
    ----------
    method: `(...) -> Any`
        The method to be decorated
    """

    def __init__(self, method: Callable) -> None:
        """
        Initializes the decorator.

        Parameters
        ----------
        method: `(...) -> Any`
            The method to be decorated
        """
        self.method = method

    def __get__(self, instance: Any, instance_class: Any) -> Any:
        return self.method(instance_class)
