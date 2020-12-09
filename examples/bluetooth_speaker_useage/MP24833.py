from ECPF.components import iterate_value_order_magnitude
from ECPF.value_filter import ValueFilter
from ECPF.components import iComponent, Component, ChainPermutation
from ECPF.value_permutator import iPermutator, ComponentPermutator, ChainPermutator
from ECPF.constants import E_SERIES
from ECPF.component_config_functs import ResistorConfiguration, CapacitorConfiguration, InductorConfiguration
import itertools
from inspect import signature
from matplotlib import pyplot as plt
from ECPF.float_representation_tools import eng_format

# Design parameters
vin = 5.0
vout = 12.0
current_led = 2.0
operating_freq = 200 * 10 ** 3

# Intermediate Calculations
r_sense = 0.198 / current_led

average_inductor_current = current_led * (1 + vout / vin)

selected_current_ripple_pp = average_inductor_current * 0.3
peak_inductor_current = average_inductor_current + 1 / 2 * selected_current_ripple_pp

inductor_value = vin * vout / (
        (vin + vout) * selected_current_ripple_pp * operating_freq)


def stat_display(
        theoretical_min, theoretical_max,
        sample_len, standard_dev, variance, skewness, mean_val, q25, median, q75
):
    # Display some good statistical information about the range of values
    return "\n".join((
        f"theoretical min: {theoretical_min}",
        f"theoretical max: {theoretical_max}",
        f"Monte-Carlo stats of the {eng_format(sample_len)} samples generated:",
        f"    std: {standard_dev}",
        f"    variance: {variance}",
        f"    skewness: {skewness}",
        f"    mean: {mean_val}",
        f"    q25: {q25}",
        f"    q50: {median}",
        f"    q75: {q75}"
    ))


def voltage_out_res_div():
    vf = ValueFilter(
        value_iterators=[
            ChainPermutator(
                components=[
                    ComponentPermutator(
                        values=(v for v in iterate_value_order_magnitude(E_SERIES["E6"], range(2, 7))),
                        tolerance=0.01
                    ),
                    ComponentPermutator(
                        values=(82, 100, 1 * 10 ** 3, 10 * 10 ** 3),
                        tolerance=0.01
                    ),
                ],
                chaining_functions=(
                    ResistorConfiguration.series, ResistorConfiguration.parallel
                )
            ),
            ChainPermutator(
                components=[
                    ComponentPermutator(
                        values=(1 * 10 ** 3),
                        tolerance=0.05
                    ),
                ],
                chaining_functions=(
                    ResistorConfiguration.series, ResistorConfiguration.parallel
                )
            ),
            ChainPermutator(
                components=[
                    ComponentPermutator(
                        values=(v for v in iterate_value_order_magnitude(E_SERIES["E6"], range(2, 7))),
                        tolerance=0.01
                    ),
                ],
                chaining_functions=(
                    ResistorConfiguration.series, ResistorConfiguration.parallel
                )
            )
        ],
        target_value=vout,
        calculation_function=lambda rovp1, trim_pot, rovp2: 1.2 * (
                float(rovp1) + float(rovp2) + float(trim_pot)
        ) / float(rovp2),
        filters=[
            lambda rovp1, trim_pot, rovp2: 1.1 * (
                    float(rovp1) + float(rovp2) + float(trim_pot)
            ) / float(rovp2),
        ],
        number_of_results=20
    )
    vf.populate_results()
    print(f"While trying to achieve a value of: {eng_format(vf.target_value)}\n"
          f"Total permutations tested:{vf.total_permutations_tested}\n"
          f"Permutations filtered: {vf.permutations_filtered}")

    for v, conf in vf:

        # Display general info about the accuracy of the configuration
        print(f"\n{'*' * 20}\nA value of {eng_format(float(v))} ({100.0 * vf.calc_error(v)}%)"
              f"was achieved with the following configuration\n{'*' * 20}\n"
              f"{stat_display(*vf.generate_stat_data(conf))}"  # Generate statistical data for the configuration
              )

        # Pull actual parameter names of the calculation function
        calc_signature = signature(vf.calculation_function)

        # Iterate over all component names, and the corresponding configuration
        for component_configuration, param_name in zip(conf, calc_signature.parameters.values()):
            print(f"{param_name} Configuration:\n{component_configuration.text_representation()}")


if __name__ == "__main__":
    print(
        f"average_inductor_current: {average_inductor_current}\n"
        f"selected_current_ripple_pp: {selected_current_ripple_pp}\n"
        f"peak_inductor_current: {peak_inductor_current}\n"
        f"inductor_value: {inductor_value}\n"
        f"r_sense: {r_sense}"
    )

    voltage_out_res_div()
