import decimal
from typing import Set, Tuple, Dict, List, Deque, Iterable, Callable, Generator
from collections import deque
from operator import mul
import itertools
import functools
import operator
import math
import random
from math import factorial

from components import iComponent, Component, ChainPermutation
from value_permutator import iPermutator, ComponentPermutator, ChainPermutator
from constants import E_SERIES
from component_config_functs import ResistorConfiguration, CapacitorConfiguration, InductorConfiguration
from numpy import percentile, std, mean
from matplotlib import pyplot as plt



class ValueFilter:
    """
    ValueFilter is the highest level class
    It is responsible for taking a list of iterable objects each of which can be converted to a float
    The values are fed positionally into the given calculation function
    """

    def __init__(self,
                 target_value: float,
                 value_iterators: Iterable[iComponent],
                 calculation_function: Callable[..., float],
                 filters: Iterable[Callable[..., bool]],
                 number_of_results: int,
                 ):
        # print(signature(calculation_function).parameters)

        # The value the calculation function aims to achieve
        self.target_value: float = target_value

        # An iterable of values to feed into the calculation function
        self.value_iterators: Iterable[iComponent] = value_iterators

        # The calculation preformed on all permutations of all value iterators
        self.calculation_function: Callable[..., float] = calculation_function

        # A list of filters to run to ensure that the values fit a certain criteria
        self.filters: Iterable[Callable[..., bool]] = filters

        # A sorted Deque of results reprenenting the permutations that are closest to the target value
        self.results: Deque[Tuple[iComponent]] = deque(maxlen=number_of_results)

        # A count taken to see how many permutations were tested
        self.total_permutations_tested: int = 0
        self.permutations_filtered: int = 0

    def calc_error(self, val):
        return math.fabs(
            (float(self.target_value) - float(val)) /
            float(self.target_value)
        )

    def process_permutation(self, permutation: Tuple[iComponent]) -> None:
        """
        :param permutation: The permutation tuple to process
        :return:
        """

        # Ensure that the first result gets added to the result deque, so there is something to compare against
        if len(self.results) == 0:
            self.results.append(permutation)
            return

        # Calculate the value, and error of the passed permutation
        perm_val = self.calculation_function(*permutation)
        perm_calc_error = self.calc_error(perm_val)

        insert_index = None

        # this currently takes O(n) time, with a binary search could take O(log(n))
        for i in range(0, len(self.results)):
            if i > len(self.results):
                insert_index = i
                break

            # Calculate the value, and error of the result being permutated over
            existing_val = self.calculation_function(*self.results[i])
            existing_calc_error = self.calc_error(existing_val)

            if perm_calc_error < existing_calc_error:
                insert_index = i
                break

        if insert_index is not None:
            if len(self.results) >= self.results.maxlen:
                self.results.pop()

            self.results.insert(insert_index, permutation)

    def populate_results(self) -> None:
        """
        Populate the result Deque with tuples of Component configurations.

        :return: None
        """
        # Reset result stats
        self.total_permutations_tested = 0
        self.permutations_filtered = 0

        # Iterate over all combinations
        for val_product in itertools.product(*self.value_iterators):
            self.total_permutations_tested += 1

            # Check if permutation is valid given filters
            perm_valid = True
            for filter_funct in self.filters:
                if not filter_funct(*val_product):
                    perm_valid = False
                    break

            # Ensure that the permutation does not violate any filters defined
            if perm_valid:
                self.process_permutation(val_product)
            else:
                self.permutations_filtered += 1

    # Statistical methods
    def theoretical_min_max(self,
                            permutation: Tuple[iComponent]
                            ) -> Tuple[float, Tuple[iComponent], float, Tuple[iComponent]]:

        theoretical_min = None
        theoretical_max = None

        min_perm = None
        max_perm = None

        perm_min_max_list = []
        for c in permutation:
            perm_min_max_list.append((c.min_val, c.max_val))

        for extreme_perm in itertools.product(*perm_min_max_list):
            extreme_perm_val = self.calculation_function(*extreme_perm)

            if (theoretical_min is None) or (theoretical_max is None):
                theoretical_min, min_perm = extreme_perm_val, extreme_perm
                theoretical_max, max_perm = extreme_perm_val, extreme_perm

            if extreme_perm_val < theoretical_min:
                theoretical_min, min_perm = extreme_perm_val, extreme_perm
            if extreme_perm_val > theoretical_max:
                theoretical_max, max_perm = extreme_perm_val, extreme_perm

        return theoretical_min, min_perm, theoretical_max, max_perm

    def generate_monte_carlo_distribution_samples(
            self, permutation: Tuple[iComponent], n_samples=500 * 10 ** 3) -> Deque[float]:
        """
        The permutation to generate the samples for
        :param permutation: The permutation to take samples and calculate the value of.
        :param n_samples: The number of monte carlo samples to generate
        :return:
        """
        sample_results = deque(maxlen=n_samples)
        for s in range(n_samples):
            permutation_samples = (v.sample() for v in permutation)
            sample_val = self.calculation_function(*permutation_samples)
            sample_results.append(sample_val)

        return sample_results

    def generate_stat_data(self, permutation: Tuple[iComponent], samples=None
                           ) -> Tuple[float, float, int, float, float, float, float, float, float, float]:
        if samples is None:
            samples = self.generate_monte_carlo_distribution_samples(permutation)

        sample_len = len(samples)

        # Get the min and max values possible for the permutation
        theoretical_min, min_perm, theoretical_max, max_perm, = self.theoretical_min_max(permutation)

        # Generate the 1st and 3rd quartile values
        q25, median, q75 = percentile(
            samples,
            [25, 50, 75],
            interpolation='midpoint'
        )
        # Generate statistical information
        standard_dev = std(samples)
        mean_val = mean(samples)
        variance = sum((samp - mean_val) ** 2 for samp in samples) / (sample_len - 1)
        skewness = sample_len / ((sample_len - 1) * (sample_len - 2)) \
                   * sum((samp - mean_val) ** 3 for samp in samples) / standard_dev ** 3

        return theoretical_min, theoretical_max, sample_len, standard_dev, variance, skewness, mean_val, q25, median, q75

    @staticmethod
    def plot_sample_distribution(samples: Iterable[float]):
        plt.hist(
            x=samples,
            bins=100,
            density=True
        )
        plt.show()

    def __iter__(self):
        for result in self.results:
            yield self.calculation_function(*result), result
