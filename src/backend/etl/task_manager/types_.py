from typing import TypedDict, Generic, TypeVar

T = TypeVar('T')


class Task(TypedDict, Generic[T]):
    id_: int
    type_: str
    data: dict[str, str]


class Response(TypedDict, Generic[T]):
    task: Task[T]
    type_: str
    status: str
    success: bool

