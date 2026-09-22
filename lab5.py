"""Build an ID3 decision tree for the classic Play Tennis dataset."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field
from typing import Any


DATASET = [
    {"Day": "D1", "Outlook": "Sunny", "Temperature": "Hot", "Humidity": "High", "Wind": "Weak", "Play Tennis": "No"},
    {"Day": "D2", "Outlook": "Sunny", "Temperature": "Hot", "Humidity": "High", "Wind": "Strong", "Play Tennis": "No"},
    {"Day": "D3", "Outlook": "Overcast", "Temperature": "Hot", "Humidity": "High", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D4", "Outlook": "Rain", "Temperature": "Mild", "Humidity": "High", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D5", "Outlook": "Rain", "Temperature": "Cool", "Humidity": "Normal", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D6", "Outlook": "Rain", "Temperature": "Cool", "Humidity": "Normal", "Wind": "Strong", "Play Tennis": "No"},
    {"Day": "D7", "Outlook": "Overcast", "Temperature": "Cool", "Humidity": "Normal", "Wind": "Strong", "Play Tennis": "Yes"},
    {"Day": "D8", "Outlook": "Sunny", "Temperature": "Mild", "Humidity": "High", "Wind": "Weak", "Play Tennis": "No"},
    {"Day": "D9", "Outlook": "Sunny", "Temperature": "Cool", "Humidity": "Normal", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D10", "Outlook": "Rain", "Temperature": "Mild", "Humidity": "Normal", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D11", "Outlook": "Sunny", "Temperature": "Mild", "Humidity": "Normal", "Wind": "Strong", "Play Tennis": "Yes"},
    {"Day": "D12", "Outlook": "Overcast", "Temperature": "Mild", "Humidity": "High", "Wind": "Strong", "Play Tennis": "Yes"},
    {"Day": "D13", "Outlook": "Overcast", "Temperature": "Hot", "Humidity": "Normal", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D14", "Outlook": "Rain", "Temperature": "Mild", "Humidity": "High", "Wind": "Strong", "Play Tennis": "No"},
]

TARGET = "Play Tennis"
FEATURES = ["Outlook", "Temperature", "Humidity", "Wind"]


@dataclass
class Node:
    """A decision node or a leaf in the ID3 tree."""

    attribute: str | None = None
    label: str | None = None
    branches: dict[str, "Node"] = field(default_factory=dict)

    @property
    def is_leaf(self) -> bool:
        return self.label is not None


def entropy(rows: list[dict[str, str]]) -> float:
    counts = Counter(row[TARGET] for row in rows)
    total = len(rows)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def information_gain(rows: list[dict[str, str]], attribute: str) -> float:
    total_entropy = entropy(rows)
    total = len(rows)
    remainder = 0.0

    for value in sorted({row[attribute] for row in rows}):
        subset = [row for row in rows if row[attribute] == value]
        remainder += len(subset) / total * entropy(subset)

    return total_entropy - remainder


def majority_label(rows: list[dict[str, str]]) -> str:
    return Counter(row[TARGET] for row in rows).most_common(1)[0][0]


def build_tree(rows: list[dict[str, str]], attributes: list[str]) -> Node:
    labels = {row[TARGET] for row in rows}
    if len(labels) == 1:
        return Node(label=next(iter(labels)))
    if not attributes:
        return Node(label=majority_label(rows))

    best_attribute = max(attributes, key=lambda attribute: information_gain(rows, attribute))
    node = Node(attribute=best_attribute)
    remaining_attributes = [attribute for attribute in attributes if attribute != best_attribute]

    for value in sorted({row[best_attribute] for row in rows}):
        subset = [row for row in rows if row[best_attribute] == value]
        node.branches[value] = build_tree(subset, remaining_attributes)

    return node


def predict(node: Node, example: dict[str, str]) -> str:
    while not node.is_leaf:
        node = node.branches[example[node.attribute]]  # type: ignore[index]
    return node.label  # type: ignore[return-value]


def print_tree(node: Node, prefix: str = "", branch_label: str | None = None, is_last: bool = True) -> None:
    connector = "`-- " if is_last else "|-- "
    if branch_label is not None:
        print(f"{prefix}{connector}{branch_label}")

    if node.is_leaf:
        print(f"{prefix}    [Leaf: {node.label}]")
        return

    if branch_label is None:
        print(node.attribute)

    values = list(node.branches.items())
    child_prefix = prefix + ("    " if is_last else "|   ")
    for index, (value, child) in enumerate(values):
        print_tree(
            child,
            prefix=child_prefix,
            branch_label=f"{node.attribute} = {value}",
            is_last=index == len(values) - 1,
        )


def main() -> None:
    root_entropy = entropy(DATASET)
    print(f"Dataset entropy: {root_entropy:.3f}")
    print("Information gain at root:")
    for feature in FEATURES:
        print(f"  {feature}: {information_gain(DATASET, feature):.3f}")

    tree = build_tree(DATASET, FEATURES)
    print("\nDecision tree:")
    print_tree(tree)

    correct = sum(predict(tree, row) == row[TARGET] for row in DATASET)
    print(f"\nTraining accuracy: {correct}/{len(DATASET)}")


if __name__ == "__main__":
    main()