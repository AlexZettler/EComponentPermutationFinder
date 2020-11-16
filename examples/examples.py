from components import iterate_value_order_magnitude
from value_filter import ValueFilter
from components import iComponent, Component, ChainPermutation
from value_permutator import iPermutator, ComponentPermutator, ChainPermutator
from constants import E_SERIES
from component_config_functs import ResistorConfiguration, CapacitorConfiguration, InductorConfiguration
import itertools
from inspect import signature
from matplotlib import pyplot as plt


def rc():
    resistor_permutator = ChainPermutator(
        components=[
            ComponentPermutator(
                values=(v for v in iterate_value_order_magnitude(
                    E_SERIES["E6"], range(8, 12))),
                tolerance=0.05
            ),
            ComponentPermutator(
                values=(v for v in iterate_value_order_magnitude(
                    E_SERIES["E6"], range(8, 12))),
                tolerance=0.05
            ),
        ],
        chaining_functions=(
            ResistorConfiguration.series,
            ResistorConfiguration.parallel,
        )
    )

    capacitor_permutator = ChainPermutator(
        components=[
            ComponentPermutator(
                values=(v for v in iterate_value_order_magnitude(
                    E_SERIES["E6"], range(-9, -6))),
                tolerance=0.0
            ),
        ],
        chaining_functions=(
            CapacitorConfiguration.series,
            CapacitorConfiguration.parallel,
        )
    )

    vf = ValueFilter(
        target_value=1.0,
        value_iterators=[resistor_permutator, capacitor_permutator],
        calculation_function=lambda x, y: float(x) * float(y),
        number_of_results=20
    )
    vf.populate_results()
    print(f"Total permutations tested: {vf.total_permutations_tested}")

    for v, conf in vf:
        calc_signature = signature(vf.calculation_function)

        r_name, c_name = calc_signature.parameters.values()
        r, c = conf

        print(f"\n{'*' * 20}\n{v} created with the following configuration\n{'*' * 20}\n")

        print(f"{r_name} Configuration:\n{r.text_representation()}")
        print(f"{c_name} Configuration:\n{c.text_representation()}")
        # print(c)


# def res_div(r1, r2) -> float:
#    result_val = float(r1) / (float(r1) + float(r2))
#    print(f"{r1}, {r2} = {result_val}")
#    return result_val


if __name__ == "__main__":
    pass
