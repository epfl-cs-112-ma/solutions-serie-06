from trees import *
import pytest

def test_branch_weight() -> None:
    b = Branch(Leaf("foo", 5), Leaf("bar", 12))
    assert b.weight == 17
    assert Branch(b, Leaf("foobar", 2)).weight == 19

def values_def[T](tree: Tree[T]) -> set[T]:
    """Definition of values, for use in tests."""
    match tree:
        case Leaf():
            return {tree.value}
        case Branch():
            return values_def(tree.left) | values_def(tree.right)
        case _:
            raise AssertionError(f"Unknown type of tree: {type(tree)}")

def values_with_paths_def[T](tree: Tree[T]) -> dict[T, Path]:
    """Definition of values_with_def, for use in tests."""
    match tree:
        case Leaf():
            return {tree.value: []}
        case Branch():
            return \
              {v: [Side.LEFT] + p for v, p in values_with_paths_def(tree.left).items()} | \
              {v: [Side.RIGHT] + p for v, p in values_with_paths_def(tree.right).items()}
        case _:
            raise AssertionError(f"Unknown type of tree: {type(tree)}")

# Some binary trees we will use in tests, comparing the efficient
# implementations to the definitions.
TEST_BIN_TREES: tuple[Tree[object], ...] = (
    Leaf("foo", 5),
    Branch(Leaf("foo", 5), Leaf("bar", 12)),
    Branch(Leaf(5, 0), Branch(Branch(Leaf(9, 0), Leaf(5, 0)), Leaf(7, 0))),
)

def test_values() -> None:
    for tree in TEST_BIN_TREES:
        assert tree.values() == values_def(tree)

def test_follow_path() -> None:
    tree = Branch(Leaf(5, 0), Branch(Branch(Leaf(9, 0), Leaf(5, 0)), Leaf(7, 0)))
    assert tree.follow_path([Side.LEFT]) == 5
    assert tree.follow_path([Side.RIGHT, Side.LEFT, Side.LEFT]) == 9
    assert tree.follow_path([Side.RIGHT, Side.LEFT, Side.RIGHT]) == 5
    assert tree.follow_path([Side.RIGHT, Side.RIGHT]) == 7

    with pytest.raises(ValueError):
        tree.follow_path([])
    with pytest.raises(ValueError):
        tree.follow_path([Side.LEFT, Side.LEFT])
    with pytest.raises(ValueError):
        tree.follow_path([Side.RIGHT, Side.LEFT])

def test_values_with_paths() -> None:
    for tree in TEST_BIN_TREES:
        assert tree.values_with_paths() == values_with_paths_def(tree)
