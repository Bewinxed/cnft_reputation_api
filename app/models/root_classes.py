import typing

T = typing.TypeVar('T')

def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))

def to_lower_camel(string: str) -> str:
    return string[0].lower() + to_camel(string)[1:]

class ListWrapper(typing.Generic[T]):
    def __init__(
        self,
        the_list: typing.Optional[list[T]] = None,
    ) -> None:
        self._wrapped_list = the_list or []

    @classmethod
    def __get_validators__(
        cls,
    ) -> typing.Generator[typing.Callable[..., typing.Self], None, None]:
        yield cls.validate

    @classmethod
    def validate(
        cls,
        value: typing.Any,
    ) -> typing.Self:
        if type(value) is cls:
            return value
        elif not isinstance(value, list[T]):
            raise TypeError(f'value must be a list or ListWrapper, not {type(value)}')

        return cls(value)

    def __getattr__(
        self,
        name: str,
    ) -> typing.Any:
        return getattr(
            self._wrapped_list,
            name,
        )