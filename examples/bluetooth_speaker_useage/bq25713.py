from ECPF.components import iterate_value_order_magnitude
from ECPF.value_filter import ValueFilter
from ECPF.value_permutator import iPermutator, ComponentPermutator, ChainPermutator
from ECPF.constants import E_SERIES
from ECPF.component_config_functs import ResistorConfiguration, CapacitorConfiguration, InductorConfiguration
from inspect import signature
from ECPF.float_representation_tools import eng_format

resistor_values_in_bom = (
    1, 10, 100,
    1 * 10 ** 3, 10 * 10 ** 3, 100 * 10 ** 3,
    1 * 10 ** 6,
    4.99, 82,
    180 * 10 ** 3, 82 * 10 ** 3
)


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


def imax_res_div():
    vf = ValueFilter(
        value_iterators=[
            ChainPermutator(
                components=[
                    ComponentPermutator(
                        values=(1, 10, 100, 1 * 10 ** 3, 10 * 10 ** 3, 100 * 10 ** 3, 1 * 10 ** 6, 4.99, 82),
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
                        values=(1, 10, 100, 1 * 10 ** 3, 10 * 10 ** 3, 100 * 10 ** 3, 1 * 10 ** 6, 4.99, 82,
                                *(v for v in iterate_value_order_magnitude(E_SERIES["E12"], range(2, 7)))),
                        tolerance=0.01
                    ),
                ],
                chaining_functions=(
                    ResistorConfiguration.series, ResistorConfiguration.parallel
                )
            )
        ],
        target_value=2.9,  # 1.0 + 40 * 3.0A * 10 * 10 ** -3,
        calculation_function=lambda ra, rb: ((6.0 * float(ra) / (float(ra) + float(rb))) - 1) / (40 * 10 * 10 ** -3),
        filters=[],
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


def call_batpresz_res_div():
    vf = ValueFilter(
        value_iterators=[
            ChainPermutator(
                components=[
                    ComponentPermutator(
                        values=resistor_values_in_bom,
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
                        values=(
                            *resistor_values_in_bom,
                            *(v for v in iterate_value_order_magnitude(E_SERIES["E12"], range(2, 7)))
                        ),
                        tolerance=0.01
                    ),
                ],
                chaining_functions=(
                    ResistorConfiguration.series, ResistorConfiguration.parallel
                )
            )
        ],
        target_value=0.55,  # 1.0 + 40 * 3.0A * 10 * 10 ** -3,
        calculation_function=lambda ra, rb: float(ra) / (float(ra) + float(rb)),
        filters=[],
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


def _40k2_resistor():
    vf = ValueFilter(
        value_iterators=[
            ChainPermutator(
                components=[
                    ComponentPermutator(
                        values=resistor_values_in_bom,
                        tolerance=0.01
                    ),
                    ComponentPermutator(
                        values=(
                            *resistor_values_in_bom,
                            *(v for v in iterate_value_order_magnitude(E_SERIES["E6"], range(2, 7)))),
                        tolerance=0.01
                    ),
                ],
                chaining_functions=(
                    ResistorConfiguration.series, ResistorConfiguration.parallel
                )
            ),

        ],
        target_value=40.2 * 10 ** 3,
        calculation_function=lambda r: r,
        filters=[],
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


def _30k_resistor():
    vf = ValueFilter(
        value_iterators=[
            ChainPermutator(
                components=[
                    ComponentPermutator(
                        values=(
                            1, 10, 100, 1 * 10 ** 3, 10 * 10 ** 3, 100 * 10 ** 3, 1 * 10 ** 6,
                            4.99, 82,
                            180 * 10 ** 3, 82 * 10 ** 3),
                        tolerance=0.01
                    ),
                    ComponentPermutator(
                        values=(
                            1, 10, 100, 1 * 10 ** 3, 10 * 10 ** 3, 100 * 10 ** 3, 1 * 10 ** 6,
                            4.99, 82,
                            180 * 10 ** 3, 82 * 10 ** 3,
                            *(v for v in iterate_value_order_magnitude(E_SERIES["E6"], range(2, 7)))),
                        tolerance=0.01
                    ),
                ],
                chaining_functions=(
                    ResistorConfiguration.series, ResistorConfiguration.parallel
                )
            ),

        ],
        target_value=30 * 10 ** 3,
        calculation_function=lambda r: r,
        filters=[],
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
    call_batpresz_res_div()
