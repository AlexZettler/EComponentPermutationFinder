"""
Defines objects that generate component permutations
"""

import decimal
from typing import Set, Tuple, Dict, List, Deque, Iterable, Callable, Generator, Any
import itertools
import functools
import operator
import math
from ECPF.components import iComponent, Component, ChainPermutation


class iPermutator:
    @property
    def permutation_count(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Generator[iComponent, None, None]:
        raise NotImplementedError


class ComponentPermutator(iPermutator):
    """
    This class simply acts as an iterator for possible values for a component that can be purchased
    """

    def __init__(self, values: Iterable, tolerance: float = 0.0):
        self.values: Iterable = values
        self.tolerance: float = tolerance

    @property
    def permutation_count(self) -> int:
        return sum(1 for x in self.values)

    def __iter__(self) -> Generator[Component, None, None]:
        for v in self.values:
            yield Component(v, self.tolerance)


class ChainPermutator(iPermutator):
    """
    This class acts as a may of chaining PermutatorComponent devices
    """

    def __init__(self, components: Iterable[ComponentPermutator], chaining_functions: Iterable[Callable]):
        self.components: Iterable[ComponentPermutator] = components
        self.chaining_functions: Iterable[Callable] = chaining_functions

    @property
    def permutation_count(self) -> int:
        return functools.reduce(operator.mul, [v.permutation_count for v in self.components], 1) * \
               sum(1 for x in self.chaining_functions) ** (sum(1 for x in self.components) - 1)

    def __iter__(self) -> Generator[ChainPermutation, None, None]:
        for chain_vals in itertools.product(*self.components):

            for funct_perm in itertools.permutations(self.chaining_functions, r=sum(1 for x in self.components) - 1):
                # print(funct_perm)

                yield ChainPermutation(chain_vals, funct_perm)  # type: ignore
