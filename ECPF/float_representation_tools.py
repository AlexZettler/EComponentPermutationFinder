str_to_decimal_places = {
    "M": 6,
    "k": 3,
    "": 0,
    "m": -3,
    "u": -6,
    "n": -9,
    "p": -12,
}

decimal_places_to_str = {v: k for k, v in str_to_decimal_places.items()}

M = 10 ** str_to_decimal_places["M"]
k = 10 ** str_to_decimal_places["k"]
m = 10 ** str_to_decimal_places["m"]
u = 10 ** str_to_decimal_places["u"]
n = 10 ** str_to_decimal_places["n"]
p = 10 ** str_to_decimal_places["p"]

str_to_eng_unit = {
    "M": M,
    "k": k,
    "m": m,
    "u": u,
    "µ": u,
    "n": n,
    "p": p
}


def eng_format(value: float, force_exp=False) -> str:
    dec_places_moved = 0

    while value >= 1000:
        value /= 1000
        dec_places_moved += 3

    while value < 1:
        value *= 1000
        dec_places_moved -= 3

    if force_exp:
        return f"{value}*10^{dec_places_moved}"

    else:
        try:
            return f"{value}{decimal_places_to_str[dec_places_moved]}"
        except KeyError:
            return f"{value}*10^{dec_places_moved}"


def sci_format(value: float) -> str:
    dec_places_moved = 0

    while value >= 10:
        value /= 10
        dec_places_moved += 1

    while value < 1:
        value *= 10
        dec_places_moved -= 1

    return f"{value}*10^{dec_places_moved}"
