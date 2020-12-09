# Electronics Component Permutation Finder
## Description:
This package simplifies the process of finding passive components for a schematic.
Practically this means finding component configurations that are closest to a target value given a calculation function.

## Why:
The value of the tool is it's ability to reuse existing components in the design leading to the following benefits:
* Reduce the number of unique components:
    * Makes ordering parts easier
    * Reduces frequency of component manufacturing EOL(end of life) product design changes.
    * Widens the range of pick and place machines able to populate the board.
    * Makes the BOM easier to look at :)
* Makes tedious "by hand" trial and error calculations easier
* Easy to get started with and extend the functionality of.
* Allows the design calculations to be referred to in the future in the case of changing, or reusing part of the design.

## Installing:
More info once on pypi

## Usage Example:
```python
from ECPF.components import iterate_value_order_magnitude
from ECPF.value_filter import ValueFilter
from ECPF.value_permutator import iPermutator, ComponentPermutator, ChainPermutator
from ECPF.constants import E_SERIES
from ECPF.component_config_functs import ResistorConfiguration, CapacitorConfiguration, InductorConfiguration
from inspect import signature
from ECPF.float_representation_tools import eng_format

# This example finds 

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
                        #*(v for v in iterate_value_order_magnitude(E_SERIES["E12"], range(2, 7)))
                    ),
                    tolerance=0.01
                ),
            ],
            chaining_functions=(
                ResistorConfiguration.series, ResistorConfiguration.parallel
            )
        )
    ],
    target_value=0.55,
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
```
Returns the following:
```
While trying to achieve a value of: 550.0m
Total permutations tested:781
Permutations filtered: 0

********************
A value of 549.4505494505495m (0.09990009990009953%)was achieved with the following configuration
********************
theoretical min: 0.5444945550544494
theoretical max: 0.5543967504665716
Monte-Carlo stats of the 500.0k samples generated:
    std: 0.002022700239755151
    variance: 4.091324442554523e-06
    skewness: -0.0009272373620062638
    mean: 0.5494490568368843
    q25: 0.5479987596537707
    q50: 0.5494486071973117
    q75: 0.5509031728580739
ra Configuration:
|      +---------+       
+------+  100.0  +------+
       +---------+      |
                        |
+-----------------------+
|                        
rb Configuration:
|      +--------+       
+------+  82.0  +------+
       +--------+      |
                       |
+----------------------+
|                       

********************
A value of 549.4505494505495m (0.09990009990009953%)was achieved with the following configuration
********************
theoretical min: 0.5444945550544495
theoretical max: 0.5543967504665716
Monte-Carlo stats of the 500.0k samples generated:
    std: 0.0020198213511608415
    variance: 4.0796864499781015e-06
    skewness: -0.004083053018769606
    mean: 0.5494487845514864
    q25: 0.5480018637339282
    q50: 0.5494517047645346
    q75: 0.5508959649484428
ra Configuration:
|      +--------+       
+------+  1.0k  +------+
       +--------+      |
                       |
+----------------------+
|                       
rb Configuration:
|      +---------------------+       
+------+  819.9999999999999  +------+
       +---------------------+      |
                                    |
+-----------------------------------+
|                                    
```


## Contributing:
Feel free to request a merge. If it a large change to the code base, please e-mail (azettler@live.com) me prior to discuss the suggestion and see if makes sense and if so how I can help.