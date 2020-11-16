import decimal
from typing import Set, Tuple, Dict, List, Deque, Iterable, Callable, Generator
from collections import deque
from operator import mul
import itertools
import functools
import operator
import math
import random
from float_representation_tools import eng_format


# from inspect import signature


class iComponent:

    @property
    def value(self) -> float:
        raise NotImplementedError

    def __float__(self) -> float:
        raise NotImplementedError

    @property
    def min_val(self) -> float:
        raise NotImplementedError

    @property
    def max_val(self) -> float:
        raise NotImplementedError

    def sample(self) -> float:
        raise NotImplementedError


class Component(iComponent):
    def __init__(self, value, tolerance):
        self._value: float = value
        self._tolerance: float = tolerance

    @property
    def value(self) -> float:
        return self._value

    def __float__(self) -> float:
        return float(self._value)

    @property
    def min_val(self) -> float:
        return self._value * (1.0 - self._tolerance)

    @property
    def max_val(self) -> float:
        return self._value * (1.0 + self._tolerance)

    def sample(self) -> float:
        return self.min_val + random.random() * (self.max_val - self.min_val)


class ChainPermutation(iComponent):
    def __init__(self, chain_vals: Tuple[Component], chain_functions: Iterable[Callable]):

        self.chain_vals: Tuple[Component] = chain_vals
        self.chain_functions = chain_functions
        self._max_val = None
        self._min_val = None

    def __str__(self):
        return f"{self.value}"

    @classmethod
    def _component_as_graphic_text(cls, component_text, text_length, prev_parallel, next_parallel):

        line1 = f"|      +{'-' * text_length}+      {'|' if prev_parallel else ' '}"
        line2 = f"+------+{component_text.center(text_length)}+------+"
        line3 = f"{'|' if next_parallel else ' '}      +{'-' * text_length}+      |"

        return "\n".join((line1, line2, line3))

    def text_representation(self):

        # Format the components in engineering notation
        val_texts: Tuple[str] = [eng_format(float(v)) for v in self.chain_vals]
        max_length = max(len(v) for v in val_texts) + 4

        # Check if the component was added in series or parallel
        parallel_components = [False]
        for v in self.chain_functions:
            if v.__name__ == "parallel":
                parallel_components.append(True)
            elif v.__name__ == "series":
                parallel_components.append(False)
            else:
                raise ValueError(
                    f"Function must be names series or parallel in order to have a text representation: {v}"
                )
        parallel_components.append(False)

        string_parts = []
        for v, prev_conf, next_conf in zip(val_texts, parallel_components, parallel_components[1:]):
            string_parts.append(self._component_as_graphic_text(v, max_length, prev_conf, next_conf))
            if next_conf is not True:
                string_parts.append(f"       {' ' * (max_length + 2)}      |")
                string_parts.append(f"+------{'-' * (max_length + 2)}------+")
                string_parts.append(f"|      {' ' * (max_length + 2)}       ")
            else:
                string_parts.append(f"|      {' ' * (max_length + 2)}      |")
        return "\n".join(string_parts)

    @property
    def value(self) -> float:
        current_value = float(self.chain_vals[0])
        for v, f in zip(self.chain_vals[1:], self.chain_functions):
            current_value = f(current_value, float(v))
        return current_value

    def __float__(self):
        return float(self.value)

    @property
    def min_val(self):
        if self._min_val is None:
            self._min_val, self._max_val = self._get_min_max()
        return self._min_val

    @property
    def max_val(self):
        if self._min_val is None:
            self._min_val, self._max_val = self._get_min_max()
        return self._max_val

    def _get_min_max(self):

        min_val = None
        max_val = None

        max_min_chain = []

        for v in self.chain_vals:
            # nominal = v.value
            max_val = v.max_val
            min_val = v.min_val
            max_min_chain.append((max_val, min_val))

        for initial_value in max_min_chain[0]:
            for extreme_vals in itertools.product(*max_min_chain[1:]):
                current_value = initial_value
                for v, f in zip(extreme_vals, self.chain_functions):
                    current_value = f(current_value, v)

                min_val = min(min_val, current_value)
                max_val = max(max_val, current_value)

        return min_val, max_val

    def sample(self) -> float:
        current_value = self.chain_vals[0].sample()
        for v, f in zip(self.chain_vals[1:], self.chain_functions):
            current_value = f(current_value, v.sample())
        return current_value


def iterate_value_order_magnitude(values, magnitude_orders):
    for v in values:
        for o in magnitude_orders:
            yield v * 10 ** o
