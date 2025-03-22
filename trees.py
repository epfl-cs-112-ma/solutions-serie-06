from __future__ import annotations

from abc import abstractmethod
from enum import Enum, auto
from typing import Final

class Side(Enum):
    LEFT = auto()
    RIGHT = auto()

type Path = list[Side]

class Tree[T]:
    # We store the weight as an attribute for all trees, so that is
    # efficient (Θ(1)) for all kinds of trees.
    # An alternative would be to define it as an abstract @property.
    weight: Final[int]
    """The weight of the tree."""

    def __init__(self, weight: int) -> None:
        self.weight = weight

    def values(self) -> set[T]:
        """Returns the set of all the values in this tree.

        leaf.values() = {left.value}
        branch.values() = branch.left.values() | branch.right.values()

        Complexity: Θ(n) where n is the total number of nodes in the tree.
        """
        result: set[T] = set()
        self._values_impl(result)
        return result

    @abstractmethod
    def _values_impl(self, result: set[T]) -> None:
        """Adds the values of this substree to the `result` set.

        Complexity: Θ(n) where n is the total number of nodes in the subtree.
        """
        ...

    def follow_path(self, path: Path) -> T:
        """Returns the value at the end of the given `path`.

        If the path does not end exactly at a `Leaf`, raises a `ValueError`.
        """
        return self._follow_path_impl(path, 0)

    @abstractmethod
    def _follow_path_impl(self, path: Path, index: int) -> T:
        """Returns the value at the end of the path `path[index:]`."""
        ...

    def values_with_paths(self) -> dict[T, Path]:
        """Returns the dict of all the values in this tree, associated with their path.

        leaf.values_with_paths() =
          {left.value: []}
        branch.values_with_paths() =
          {v: [Side.LEFT] + p for v, p in branch.left.values_with_paths().items()} |
          {v: [Side.RIGHT] + p for v, p in branch.right.values_with_paths().items()}
        """
        result: dict[T, Path] = {}
        self._values_with_paths_impl([], result)
        return result

    @abstractmethod
    def _values_with_paths_impl(self, path: Path, result: dict[T, Path]) -> None:
        """Adds the values with paths of this substree to the `result` dict.

        `path` must be the path required to reach the `self` node.
        `path` will be mutated after the call to this method. A copy must be
        made if it is stored for future use. `path` must not have changed when
        this method returns.
        """
        ...

class Leaf[T](Tree[T]):
    # https://github.com/python/mypy/issues/8982
    # We cannot declare `value` here because we want to be Final *and* refer
    # to the type variable T. Mypy does not like that, unfortunately.
    def __init__(self, value: T, weight: int) -> None:
        super().__init__(weight)
        self.value: Final[T] = value # we declare it as Final[T] here as a workaround

    def __repr__(self) -> str:
        return f"Leaf({repr(self.value)})"

    def _values_impl(self, result: set[T]) -> None:
        result.add(self.value)

    def _follow_path_impl(self, path: Path, index: int) -> T:
        if index != len(path):
            raise ValueError(f"Path too long; remaining elements: {repr(path[index:])}")
        return self.value

    def _values_with_paths_impl(self, path: Path, result: dict[T, Path]) -> None:
        result[self.value] = path.copy()

class Branch[T](Tree[T]):
    # Same mypy issue
    def __init__(self, left: Tree[T], right: Tree[T]) -> None:
        super().__init__(left.weight + right.weight)
        self.left: Final[Tree[T]] = left
        self.right: Final[Tree[T]] = right

    def __repr__(self) -> str:
        return f"Branch({repr(self.left)}, {repr(self.right)})"

    def _values_impl(self, result: set[T]) -> None:
        self.left._values_impl(result)
        self.right._values_impl(result)

    def _follow_path_impl(self, path: Path, index: int) -> T:
        if index >= len(path):
            raise ValueError(f"Path too short: sub-tree left to explore: {repr(self)}")
        if path[index] == Side.LEFT:
            return self.left._follow_path_impl(path, index + 1)
        else:
            return self.right._follow_path_impl(path, index + 1)

    def _values_with_paths_impl(self, path: Path, result: dict[T, Path]) -> None:
        path.append(Side.LEFT)
        self.left._values_with_paths_impl(path, result)
        path.pop()
        path.append(Side.RIGHT)
        self.right._values_with_paths_impl(path, result)
        path.pop()
