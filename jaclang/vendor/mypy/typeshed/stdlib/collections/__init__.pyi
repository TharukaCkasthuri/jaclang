import sys
from _collections_abc import dict_items, dict_keys, dict_values
from _typeshed import (
    SupportsItems,
    SupportsKeysAndGetItem,
    SupportsRichComparison,
    SupportsRichComparisonT,
)
from typing import Any, Generic, NoReturn, TypeVar, overload
from typing_extensions import Self, SupportsIndex, final

if sys.version_info >= (3, 9):
    from types import GenericAlias

if sys.version_info >= (3, 10):
    from collections.abc import (
        Callable,
        ItemsView,
        Iterable,
        Iterator,
        KeysView,
        Mapping,
        MutableMapping,
        MutableSequence,
        Reversible,
        Sequence,
        ValuesView,
    )
else:
    from _collections_abc import *

__all__ = [
    "ChainMap",
    "Counter",
    "OrderedDict",
    "UserDict",
    "UserList",
    "UserString",
    "defaultdict",
    "deque",
    "namedtuple",
]

_S = TypeVar("_S")
_T = TypeVar("_T")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_KT_co = TypeVar("_KT_co", covariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)

# namedtuple is special-cased in the type checker; the initializer is ignored.
def namedtuple(
    typename: str,
    field_names: str | Iterable[str],
    *,
    rename: bool = False,
    module: str | None = None,
    defaults: Iterable[Any] | None = None,
) -> type[tuple[Any, ...]]: ...

class UserDict(MutableMapping[_KT, _VT]):
    data: dict[_KT, _VT]
    # __init__ should be kept roughly in line with `dict.__init__`, which has the same semantics
    @overload
    def __init__(self, __dict: None = None) -> None: ...
    @overload
    def __init__(
        self: UserDict[str, _VT], __dict: None = None, **kwargs: _VT
    ) -> None: ...
    @overload
    def __init__(self, __dict: SupportsKeysAndGetItem[_KT, _VT]) -> None: ...
    @overload
    def __init__(
        self: UserDict[str, _VT],
        __dict: SupportsKeysAndGetItem[str, _VT],
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def __init__(self, __iterable: Iterable[tuple[_KT, _VT]]) -> None: ...
    @overload
    def __init__(
        self: UserDict[str, _VT], __iterable: Iterable[tuple[str, _VT]], **kwargs: _VT
    ) -> None: ...
    @overload
    def __init__(self: UserDict[str, str], __iterable: Iterable[list[str]]) -> None: ...
    @overload
    def __init__(
        self: UserDict[bytes, bytes], __iterable: Iterable[list[bytes]]
    ) -> None: ...
    def __len__(self) -> int: ...
    def __getitem__(self, key: _KT) -> _VT: ...
    def __setitem__(self, key: _KT, item: _VT) -> None: ...
    def __delitem__(self, key: _KT) -> None: ...
    def __iter__(self) -> Iterator[_KT]: ...
    def __contains__(self, key: object) -> bool: ...
    def copy(self) -> Self: ...
    def __copy__(self) -> Self: ...

    # `UserDict.fromkeys` has the same semantics as `dict.fromkeys`, so should be kept in line with `dict.fromkeys`.
    # TODO: Much like `dict.fromkeys`, the true signature of `UserDict.fromkeys` is inexpressible in the current type system.
    # See #3800 & https://github.com/python/typing/issues/548#issuecomment-683336963.
    @classmethod
    @overload
    def fromkeys(
        cls, iterable: Iterable[_T], value: None = None
    ) -> UserDict[_T, Any | None]: ...
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_T], value: _S) -> UserDict[_T, _S]: ...
    if sys.version_info >= (3, 9):
        @overload
        def __or__(self, other: UserDict[_KT, _VT] | dict[_KT, _VT]) -> Self: ...
        @overload
        def __or__(
            self, other: UserDict[_T1, _T2] | dict[_T1, _T2]
        ) -> UserDict[_KT | _T1, _VT | _T2]: ...
        @overload
        def __ror__(self, other: UserDict[_KT, _VT] | dict[_KT, _VT]) -> Self: ...
        @overload
        def __ror__(
            self, other: UserDict[_T1, _T2] | dict[_T1, _T2]
        ) -> UserDict[_KT | _T1, _VT | _T2]: ...
        # UserDict.__ior__ should be kept roughly in line with MutableMapping.update()
        @overload  # type: ignore[misc]
        def __ior__(self, other: SupportsKeysAndGetItem[_KT, _VT]) -> Self: ...
        @overload
        def __ior__(self, other: Iterable[tuple[_KT, _VT]]) -> Self: ...
    if sys.version_info >= (3, 12):
        @overload
        def get(self, key: _KT, default: None = None) -> _VT | None: ...
        @overload
        def get(self, key: _KT, default: _T) -> _VT | _T: ...

class UserList(MutableSequence[_T]):
    data: list[_T]
    @overload
    def __init__(self, initlist: None = None) -> None: ...
    @overload
    def __init__(self, initlist: Iterable[_T]) -> None: ...
    def __lt__(self, other: list[_T] | UserList[_T]) -> bool: ...
    def __le__(self, other: list[_T] | UserList[_T]) -> bool: ...
    def __gt__(self, other: list[_T] | UserList[_T]) -> bool: ...
    def __ge__(self, other: list[_T] | UserList[_T]) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __contains__(self, item: object) -> bool: ...
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, i: SupportsIndex) -> _T: ...
    @overload
    def __getitem__(self, i: slice) -> Self: ...
    @overload
    def __setitem__(self, i: SupportsIndex, item: _T) -> None: ...
    @overload
    def __setitem__(self, i: slice, item: Iterable[_T]) -> None: ...
    def __delitem__(self, i: SupportsIndex | slice) -> None: ...
    def __add__(self, other: Iterable[_T]) -> Self: ...
    def __radd__(self, other: Iterable[_T]) -> Self: ...
    def __iadd__(self, other: Iterable[_T]) -> Self: ...
    def __mul__(self, n: int) -> Self: ...
    def __rmul__(self, n: int) -> Self: ...
    def __imul__(self, n: int) -> Self: ...
    def append(self, item: _T) -> None: ...
    def insert(self, i: int, item: _T) -> None: ...
    def pop(self, i: int = -1) -> _T: ...
    def remove(self, item: _T) -> None: ...
    def copy(self) -> Self: ...
    def __copy__(self) -> Self: ...
    def count(self, item: _T) -> int: ...
    # All arguments are passed to `list.index` at runtime, so the signature should be kept in line with `list.index`.
    def index(
        self, item: _T, __start: SupportsIndex = 0, __stop: SupportsIndex = sys.maxsize
    ) -> int: ...
    # All arguments are passed to `list.sort` at runtime, so the signature should be kept in line with `list.sort`.
    @overload
    def sort(
        self: UserList[SupportsRichComparisonT],
        *,
        key: None = None,
        reverse: bool = False,
    ) -> None: ...
    @overload
    def sort(
        self, *, key: Callable[[_T], SupportsRichComparison], reverse: bool = False
    ) -> None: ...
    def extend(self, other: Iterable[_T]) -> None: ...

class UserString(Sequence[UserString]):
    data: str
    def __init__(self, seq: object) -> None: ...
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __complex__(self) -> complex: ...
    def __getnewargs__(self) -> tuple[str]: ...
    def __lt__(self, string: str | UserString) -> bool: ...
    def __le__(self, string: str | UserString) -> bool: ...
    def __gt__(self, string: str | UserString) -> bool: ...
    def __ge__(self, string: str | UserString) -> bool: ...
    def __eq__(self, string: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __contains__(self, char: object) -> bool: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: SupportsIndex | slice) -> Self: ...
    def __iter__(self) -> Iterator[Self]: ...
    def __reversed__(self) -> Iterator[Self]: ...
    def __add__(self, other: object) -> Self: ...
    def __radd__(self, other: object) -> Self: ...
    def __mul__(self, n: int) -> Self: ...
    def __rmul__(self, n: int) -> Self: ...
    def __mod__(self, args: Any) -> Self: ...
    if sys.version_info >= (3, 8):
        def __rmod__(self, template: object) -> Self: ...
    else:
        def __rmod__(self, format: Any) -> Self: ...

    def capitalize(self) -> Self: ...
    def casefold(self) -> Self: ...
    def center(self, width: int, *args: Any) -> Self: ...
    def count(
        self, sub: str | UserString, start: int = 0, end: int = sys.maxsize
    ) -> int: ...
    if sys.version_info >= (3, 8):
        def encode(
            self: UserString,
            encoding: str | None = "utf-8",
            errors: str | None = "strict",
        ) -> bytes: ...
    else:
        def encode(
            self, encoding: str | None = None, errors: str | None = None
        ) -> Self: ...

    def endswith(
        self,
        suffix: str | tuple[str, ...],
        start: int | None = 0,
        end: int | None = sys.maxsize,
    ) -> bool: ...
    def expandtabs(self, tabsize: int = 8) -> Self: ...
    def find(
        self, sub: str | UserString, start: int = 0, end: int = sys.maxsize
    ) -> int: ...
    def format(self, *args: Any, **kwds: Any) -> str: ...
    def format_map(self, mapping: Mapping[str, Any]) -> str: ...
    def index(self, sub: str, start: int = 0, end: int = sys.maxsize) -> int: ...
    def isalpha(self) -> bool: ...
    def isalnum(self) -> bool: ...
    def isdecimal(self) -> bool: ...
    def isdigit(self) -> bool: ...
    def isidentifier(self) -> bool: ...
    def islower(self) -> bool: ...
    def isnumeric(self) -> bool: ...
    def isprintable(self) -> bool: ...
    def isspace(self) -> bool: ...
    def istitle(self) -> bool: ...
    def isupper(self) -> bool: ...
    def isascii(self) -> bool: ...
    def join(self, seq: Iterable[str]) -> str: ...
    def ljust(self, width: int, *args: Any) -> Self: ...
    def lower(self) -> Self: ...
    def lstrip(self, chars: str | None = None) -> Self: ...
    maketrans = str.maketrans
    def partition(self, sep: str) -> tuple[str, str, str]: ...
    if sys.version_info >= (3, 9):
        def removeprefix(self, __prefix: str | UserString) -> Self: ...
        def removesuffix(self, __suffix: str | UserString) -> Self: ...

    def replace(
        self, old: str | UserString, new: str | UserString, maxsplit: int = -1
    ) -> Self: ...
    def rfind(
        self, sub: str | UserString, start: int = 0, end: int = sys.maxsize
    ) -> int: ...
    def rindex(
        self, sub: str | UserString, start: int = 0, end: int = sys.maxsize
    ) -> int: ...
    def rjust(self, width: int, *args: Any) -> Self: ...
    def rpartition(self, sep: str) -> tuple[str, str, str]: ...
    def rstrip(self, chars: str | None = None) -> Self: ...
    def split(self, sep: str | None = None, maxsplit: int = -1) -> list[str]: ...
    def rsplit(self, sep: str | None = None, maxsplit: int = -1) -> list[str]: ...
    def splitlines(self, keepends: bool = False) -> list[str]: ...
    def startswith(
        self,
        prefix: str | tuple[str, ...],
        start: int | None = 0,
        end: int | None = sys.maxsize,
    ) -> bool: ...
    def strip(self, chars: str | None = None) -> Self: ...
    def swapcase(self) -> Self: ...
    def title(self) -> Self: ...
    def translate(self, *args: Any) -> Self: ...
    def upper(self) -> Self: ...
    def zfill(self, width: int) -> Self: ...

class deque(MutableSequence[_T]):
    @property
    def maxlen(self) -> int | None: ...
    @overload
    def __init__(self, *, maxlen: int | None = None) -> None: ...
    @overload
    def __init__(self, iterable: Iterable[_T], maxlen: int | None = None) -> None: ...
    def append(self, __x: _T) -> None: ...
    def appendleft(self, __x: _T) -> None: ...
    def copy(self) -> Self: ...
    def count(self, __x: _T) -> int: ...
    def extend(self, __iterable: Iterable[_T]) -> None: ...
    def extendleft(self, __iterable: Iterable[_T]) -> None: ...
    def insert(self, __i: int, __x: _T) -> None: ...
    def index(self, __x: _T, __start: int = 0, __stop: int = ...) -> int: ...
    def pop(self) -> _T: ...  # type: ignore[override]
    def popleft(self) -> _T: ...
    def remove(self, __value: _T) -> None: ...
    def rotate(self, __n: int = 1) -> None: ...
    def __copy__(self) -> Self: ...
    def __len__(self) -> int: ...
    # These methods of deque don't take slices, unlike MutableSequence, hence the type: ignores
    def __getitem__(self, __key: SupportsIndex) -> _T: ...  # type: ignore[override]
    def __setitem__(self, __key: SupportsIndex, __value: _T) -> None: ...  # type: ignore[override]
    def __delitem__(self, __key: SupportsIndex) -> None: ...  # type: ignore[override]
    def __contains__(self, __key: object) -> bool: ...
    def __reduce__(self) -> tuple[type[Self], tuple[()], None, Iterator[_T]]: ...
    def __iadd__(self, __value: Iterable[_T]) -> Self: ...
    def __add__(self, __value: Self) -> Self: ...
    def __mul__(self, __value: int) -> Self: ...
    def __imul__(self, __value: int) -> Self: ...
    def __lt__(self, __value: deque[_T]) -> bool: ...
    def __le__(self, __value: deque[_T]) -> bool: ...
    def __gt__(self, __value: deque[_T]) -> bool: ...
    def __ge__(self, __value: deque[_T]) -> bool: ...
    def __eq__(self, __value: object) -> bool: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, __item: Any) -> GenericAlias: ...

class Counter(dict[_T, int], Generic[_T]):
    @overload
    def __init__(self, __iterable: None = None) -> None: ...
    @overload
    def __init__(
        self: Counter[str], __iterable: None = None, **kwargs: int
    ) -> None: ...
    @overload
    def __init__(self, __mapping: SupportsKeysAndGetItem[_T, int]) -> None: ...
    @overload
    def __init__(self, __iterable: Iterable[_T]) -> None: ...
    def copy(self) -> Self: ...
    def elements(self) -> Iterator[_T]: ...
    def most_common(self, n: int | None = None) -> list[tuple[_T, int]]: ...
    @classmethod
    def fromkeys(cls, iterable: Any, v: int | None = None) -> NoReturn: ...  # type: ignore[override]
    @overload
    def subtract(self, __iterable: None = None) -> None: ...
    @overload
    def subtract(self, __mapping: Mapping[_T, int]) -> None: ...
    @overload
    def subtract(self, __iterable: Iterable[_T]) -> None: ...
    # Unlike dict.update(), use Mapping instead of SupportsKeysAndGetItem for the first overload
    # (source code does an `isinstance(other, Mapping)` check)
    #
    # The second overload is also deliberately different to dict.update()
    # (if it were `Iterable[_T] | Iterable[tuple[_T, int]]`,
    # the tuples would be added as keys, breaking type safety)
    @overload  # type: ignore[override]
    def update(self, __m: Mapping[_T, int], **kwargs: int) -> None: ...
    @overload
    def update(self, __iterable: Iterable[_T], **kwargs: int) -> None: ...
    @overload
    def update(self, __iterable: None = None, **kwargs: int) -> None: ...
    def __missing__(self, key: _T) -> int: ...
    def __delitem__(self, elem: object) -> None: ...
    if sys.version_info >= (3, 10):
        def __eq__(self, other: object) -> bool: ...
        def __ne__(self, other: object) -> bool: ...

    def __add__(self, other: Counter[_S]) -> Counter[_T | _S]: ...
    def __sub__(self, other: Counter[_T]) -> Counter[_T]: ...
    def __and__(self, other: Counter[_T]) -> Counter[_T]: ...
    def __or__(self, other: Counter[_S]) -> Counter[_T | _S]: ...  # type: ignore[override]
    def __pos__(self) -> Counter[_T]: ...
    def __neg__(self) -> Counter[_T]: ...
    # several type: ignores because __iadd__ is supposedly incompatible with __add__, etc.
    def __iadd__(self, other: SupportsItems[_T, int]) -> Self: ...  # type: ignore[misc]
    def __isub__(self, other: SupportsItems[_T, int]) -> Self: ...
    def __iand__(self, other: SupportsItems[_T, int]) -> Self: ...
    def __ior__(self, other: SupportsItems[_T, int]) -> Self: ...  # type: ignore[override,misc]
    if sys.version_info >= (3, 10):
        def total(self) -> int: ...
        def __le__(self, other: Counter[Any]) -> bool: ...
        def __lt__(self, other: Counter[Any]) -> bool: ...
        def __ge__(self, other: Counter[Any]) -> bool: ...
        def __gt__(self, other: Counter[Any]) -> bool: ...

# The pure-Python implementations of the "views" classes
# These are exposed at runtime in `collections/__init__.py`
class _OrderedDictKeysView(KeysView[_KT_co], Reversible[_KT_co]):
    def __reversed__(self) -> Iterator[_KT_co]: ...

class _OrderedDictItemsView(
    ItemsView[_KT_co, _VT_co], Reversible[tuple[_KT_co, _VT_co]]
):
    def __reversed__(self) -> Iterator[tuple[_KT_co, _VT_co]]: ...

class _OrderedDictValuesView(ValuesView[_VT_co], Reversible[_VT_co]):
    def __reversed__(self) -> Iterator[_VT_co]: ...

# The C implementations of the "views" classes
# (At runtime, these are called `odict_keys`, `odict_items` and `odict_values`,
# but they are not exposed anywhere)
# pyright doesn't have a specific error code for subclassing error!
@final
class _odict_keys(dict_keys[_KT_co, _VT_co], Reversible[_KT_co]):  # type: ignore[misc]  # pyright: ignore
    def __reversed__(self) -> Iterator[_KT_co]: ...

@final
class _odict_items(dict_items[_KT_co, _VT_co], Reversible[tuple[_KT_co, _VT_co]]):  # type: ignore[misc]  # pyright: ignore
    def __reversed__(self) -> Iterator[tuple[_KT_co, _VT_co]]: ...

@final
class _odict_values(dict_values[_KT_co, _VT_co], Reversible[_VT_co], Generic[_KT_co, _VT_co]):  # type: ignore[misc]  # pyright: ignore
    def __reversed__(self) -> Iterator[_VT_co]: ...

class OrderedDict(dict[_KT, _VT], Reversible[_KT], Generic[_KT, _VT]):
    def popitem(self, last: bool = True) -> tuple[_KT, _VT]: ...
    def move_to_end(self, key: _KT, last: bool = True) -> None: ...
    def copy(self) -> Self: ...
    def __reversed__(self) -> Iterator[_KT]: ...
    def keys(self) -> _odict_keys[_KT, _VT]: ...
    def items(self) -> _odict_items[_KT, _VT]: ...
    def values(self) -> _odict_values[_KT, _VT]: ...
    # The signature of OrderedDict.fromkeys should be kept in line with `dict.fromkeys`, modulo positional-only differences.
    # Like dict.fromkeys, its true signature is not expressible in the current type system.
    # See #3800 & https://github.com/python/typing/issues/548#issuecomment-683336963.
    @classmethod
    @overload
    def fromkeys(
        cls, iterable: Iterable[_T], value: None = None
    ) -> OrderedDict[_T, Any | None]: ...
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_T], value: _S) -> OrderedDict[_T, _S]: ...
    # Keep OrderedDict.setdefault in line with MutableMapping.setdefault, modulo positional-only differences.
    @overload
    def setdefault(
        self: OrderedDict[_KT, _T | None], key: _KT, default: None = None
    ) -> _T | None: ...
    @overload
    def setdefault(self, key: _KT, default: _VT) -> _VT: ...
    # Same as dict.pop, but accepts keyword arguments
    @overload
    def pop(self, key: _KT) -> _VT: ...
    @overload
    def pop(self, key: _KT, default: _VT) -> _VT: ...
    @overload
    def pop(self, key: _KT, default: _T) -> _VT | _T: ...
    def __eq__(self, __value: object) -> bool: ...
    if sys.version_info >= (3, 9):
        @overload
        def __or__(self, __value: dict[_KT, _VT]) -> Self: ...
        @overload
        def __or__(
            self, __value: dict[_T1, _T2]
        ) -> OrderedDict[_KT | _T1, _VT | _T2]: ...
        @overload
        def __ror__(self, __value: dict[_KT, _VT]) -> Self: ...
        @overload
        def __ror__(self, __value: dict[_T1, _T2]) -> OrderedDict[_KT | _T1, _VT | _T2]: ...  # type: ignore[misc]

class defaultdict(dict[_KT, _VT]):
    default_factory: Callable[[], _VT] | None
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self: defaultdict[str, _VT], **kwargs: _VT) -> None: ...
    @overload
    def __init__(self, __default_factory: Callable[[], _VT] | None) -> None: ...
    @overload
    def __init__(
        self: defaultdict[str, _VT],
        __default_factory: Callable[[], _VT] | None,
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def __init__(
        self,
        __default_factory: Callable[[], _VT] | None,
        __map: SupportsKeysAndGetItem[_KT, _VT],
    ) -> None: ...
    @overload
    def __init__(
        self: defaultdict[str, _VT],
        __default_factory: Callable[[], _VT] | None,
        __map: SupportsKeysAndGetItem[str, _VT],
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def __init__(
        self,
        __default_factory: Callable[[], _VT] | None,
        __iterable: Iterable[tuple[_KT, _VT]],
    ) -> None: ...
    @overload
    def __init__(
        self: defaultdict[str, _VT],
        __default_factory: Callable[[], _VT] | None,
        __iterable: Iterable[tuple[str, _VT]],
        **kwargs: _VT,
    ) -> None: ...
    def __missing__(self, __key: _KT) -> _VT: ...
    def __copy__(self) -> Self: ...
    def copy(self) -> Self: ...
    if sys.version_info >= (3, 9):
        @overload
        def __or__(self, __value: dict[_KT, _VT]) -> Self: ...
        @overload
        def __or__(
            self, __value: dict[_T1, _T2]
        ) -> defaultdict[_KT | _T1, _VT | _T2]: ...
        @overload
        def __ror__(self, __value: dict[_KT, _VT]) -> Self: ...
        @overload
        def __ror__(self, __value: dict[_T1, _T2]) -> defaultdict[_KT | _T1, _VT | _T2]: ...  # type: ignore[misc]

class ChainMap(MutableMapping[_KT, _VT]):
    maps: list[MutableMapping[_KT, _VT]]
    def __init__(self, *maps: MutableMapping[_KT, _VT]) -> None: ...
    def new_child(self, m: MutableMapping[_KT, _VT] | None = None) -> Self: ...
    @property
    def parents(self) -> Self: ...
    def __setitem__(self, key: _KT, value: _VT) -> None: ...
    def __delitem__(self, key: _KT) -> None: ...
    def __getitem__(self, key: _KT) -> _VT: ...
    def __iter__(self) -> Iterator[_KT]: ...
    def __len__(self) -> int: ...
    def __contains__(self, key: object) -> bool: ...
    @overload
    def get(self, key: _KT, default: None = None) -> _VT | None: ...
    @overload
    def get(self, key: _KT, default: _T) -> _VT | _T: ...
    def __missing__(self, key: _KT) -> _VT: ...  # undocumented
    def __bool__(self) -> bool: ...
    # Keep ChainMap.setdefault in line with MutableMapping.setdefault, modulo positional-only differences.
    @overload
    def setdefault(
        self: ChainMap[_KT, _T | None], key: _KT, default: None = None
    ) -> _T | None: ...
    @overload
    def setdefault(self, key: _KT, default: _VT) -> _VT: ...
    @overload
    def pop(self, key: _KT) -> _VT: ...
    @overload
    def pop(self, key: _KT, default: _VT) -> _VT: ...
    @overload
    def pop(self, key: _KT, default: _T) -> _VT | _T: ...
    def copy(self) -> Self: ...
    __copy__ = copy
    # All arguments to `fromkeys` are passed to `dict.fromkeys` at runtime, so the signature should be kept in line with `dict.fromkeys`.
    @classmethod
    @overload
    def fromkeys(
        cls, iterable: Iterable[_T], __value: None = None
    ) -> ChainMap[_T, Any | None]: ...
    @classmethod
    @overload
    def fromkeys(cls, __iterable: Iterable[_T], __value: _S) -> ChainMap[_T, _S]: ...
    if sys.version_info >= (3, 9):
        @overload
        def __or__(self, other: Mapping[_KT, _VT]) -> Self: ...
        @overload
        def __or__(
            self, other: Mapping[_T1, _T2]
        ) -> ChainMap[_KT | _T1, _VT | _T2]: ...
        @overload
        def __ror__(self, other: Mapping[_KT, _VT]) -> Self: ...
        @overload
        def __ror__(
            self, other: Mapping[_T1, _T2]
        ) -> ChainMap[_KT | _T1, _VT | _T2]: ...
        # ChainMap.__ior__ should be kept roughly in line with MutableMapping.update()
        @overload  # type: ignore[misc]
        def __ior__(self, other: SupportsKeysAndGetItem[_KT, _VT]) -> Self: ...
        @overload
        def __ior__(self, other: Iterable[tuple[_KT, _VT]]) -> Self: ...
