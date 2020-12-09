from ECPF.components import iterate_value_order_magnitude
from ECPF.value_filter import ValueFilter
from ECPF.value_permutator import iPermutator, ComponentPermutator, ChainPermutator
from ECPF.constants import E_SERIES
from ECPF.component_config_functs import ResistorConfiguration, CapacitorConfiguration
import itertools
from inspect import signature
from ECPF.float_representation_tools import eng_format

vin = 5.0
vout = 12.0

c_out = 1120.1 * 10 ** -6
inductance = 6.8 * 10 ** -6
i_out = 1.8

r_comp_val = 45 * vin * vout * c_out / (inductance * i_out)
c_comp_val = 30 * vout * inductance * i_out / (vin ** 2 * r_comp_val)


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


def current_source_vdiv():
    vf = ValueFilter(
        value_iterators=[
            ChainPermutator(
                components=[
                    ComponentPermutator(
                        values=(v for v in iterate_value_order_magnitude(E_SERIES["E6"], range(3, 7))),
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
                        values=(1000,),
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
                        values=(v for v in iterate_value_order_magnitude(E_SERIES["E6"], range(3, 7))),
                        tolerance=0.05
                    ),
                ],
                chaining_functions=(
                    ResistorConfiguration.series, ResistorConfiguration.parallel
                )
            )
        ],
        target_value=1.8,
        calculation_function=lambda r1, r2, r3: 3.3 * (float(r1) + float(r2) / 2) / (float(r1) + float(r2) + float(r3)),
        filters=[
            lambda r1, r2, r3: (float(r1) + float(r2) + float(r3)) >= 7 * 10 ** 3,
            lambda r1, r2, r3: (float(r1) + float(r2) + float(r3)) <= 20 * 10 ** 3,
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


def voltage_out_res_div():
    vf = ValueFilter(
        value_iterators=[
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
            ),
            ChainPermutator(
                components=[
                    ComponentPermutator(
                        values=(1000,),
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
        calculation_function=lambda r1, r2, r3: 0.8 * (float(r1) + float(r2) + float(r3)) / (float(r1) + float(r2) / 2),
        filters=[
            lambda r1, r2, r3: (float(r1) + float(r2) + float(r3)) <= 200 * 10 ** 3,
            lambda r1, r2, r3: float(r1) >= 2.0 * float(r2),
            lambda r1, r2, r3: float(r1) <= 8.0 * float(r2),
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


def r_comp():
    vf = ValueFilter(
        value_iterators=[
            ChainPermutator(
                components=[
                    ComponentPermutator(
                        values=(v for v in iterate_value_order_magnitude(E_SERIES["E6"], range(2, 7))),
                        tolerance=0.05
                    ),
                    ComponentPermutator(
                        values=(v for v in iterate_value_order_magnitude(E_SERIES["E6"], range(2, 7))),
                        tolerance=0.05
                    ),
                ],
                chaining_functions=(
                    ResistorConfiguration.series, ResistorConfiguration.parallel
                )
            ),

        ],
        target_value=r_comp_val,
        calculation_function=lambda r: r,
        filters=[],
        number_of_results=10
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


def c_comp():
    vf = ValueFilter(
        value_iterators=[
            ChainPermutator(
                components=[
                    ComponentPermutator(
                        values=(v for v in iterate_value_order_magnitude(E_SERIES["E6"], range(-12, -6))),
                        tolerance=0.05
                    ),
                    ComponentPermutator(
                        values=(v for v in iterate_value_order_magnitude(E_SERIES["E6"], range(-12, -6))),
                        tolerance=0.05
                    ),
                ],
                chaining_functions=(
                    CapacitorConfiguration.series, CapacitorConfiguration.parallel
                )
            ),

        ],
        target_value=c_comp_val,
        calculation_function=lambda c: c,
        filters=[
        ],
        number_of_results=10
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
    c_comp()
