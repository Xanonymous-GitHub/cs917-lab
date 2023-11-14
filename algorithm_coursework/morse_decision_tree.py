from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Optional, Final, final

# TODO: migrate to 3.12 generic feature.
_T = TypeVar('_T', covariant=True)

SHORT_SIGN: Final[str] = '.'
LONG_SIGN: Final[str] = '-'


@dataclass
class Node:
    value: _T
    parent: Optional[Node]
    left: Optional[Node] = None
    right: Optional[Node] = None
    answer: Optional[str] = None

    def __repr__(self) -> str:
        from pprint import pformat

        if self.is_leaf:
            return str(self.value)
        return pformat({f"{self.value}": (self.left, self.right)}, indent=1)

    @property
    @final
    def is_leaf(self) -> bool:
        return bool(self.left is None and self.right is None)


class MorseDecisionTree:
    root: Final[Node] = Node(value=None, parent=None)

    def traverse_nearest_of(self, /, *, morse_signs: str) -> tuple[Node, int]:
        current_node = self.root
        steps = 0

        for sign in morse_signs:
            if sign == SHORT_SIGN:
                if current_node.left is None:
                    return current_node, steps
                current_node = current_node.left
                steps += 1
            elif sign == LONG_SIGN:
                if current_node.right is None:
                    return current_node, steps
                current_node = current_node.right
                steps += 1
            else:
                raise ValueError(f"Invalid sign: {sign}")

        return current_node, steps

    @final
    def insert(self, /, *, morse_signs: str, answer: str) -> None:
        current_node, steps = self.traverse_nearest_of(morse_signs=morse_signs)

        for sign in morse_signs[steps:]:
            if sign == SHORT_SIGN:
                current_node.left = Node(value=sign, parent=current_node)
                current_node = current_node.left
            elif sign == LONG_SIGN:
                current_node.right = Node(value=sign, parent=current_node)
                current_node = current_node.right
            else:
                raise ValueError(f"Invalid sign: {sign}")

        current_node.answer = answer

    @final
    def find_nearest_node(self, /, *, morse_signs: str) -> Optional[Node]:
        current_node = self.root
        decisions = (SHORT_SIGN, LONG_SIGN)

        for sign in morse_signs:
            if sign not in decisions:
                raise ValueError(f"Invalid sign: {sign}")

            direction = 'left' if sign == SHORT_SIGN else 'right'
            current_child = getattr(current_node, direction)

            if current_child is None:
                return current_node

            current_node = current_child

        return current_node
