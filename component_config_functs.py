"""
This function defines component configuration functions to be used to simplify the writing of value permutators.
"""


class iConfiguration:
    """
    Interface defining possible configurations that components could have
    """

    @staticmethod
    def series(v1: float, v2: float) -> float:
        raise NotImplementedError

    @staticmethod
    def parallel(v1: float, v2: float) -> float:
        raise NotImplementedError


class ResistorConfiguration(iConfiguration):
    """
    Resistor configurations
    """
    @staticmethod
    def series(v1: float, v2: float) -> float:
        return v1 + v2

    @staticmethod
    def parallel(v1: float, v2: float) -> float:
        return v1 * v2 / (v1 + v2)


class CapacitorConfiguration(iConfiguration):
    """
    Capacitor configurations
    """
    @staticmethod
    def series(v1: float, v2: float) -> float:
        return v1 * v2 / (v1 + v2)

    @staticmethod
    def parallel(v1: float, v2: float) -> float:
        return v1 + v2


class InductorConfiguration(iConfiguration):
    """
    Inductor configurations
    """
    @staticmethod
    def series(v1: float, v2: float) -> float:
        return v1 + v2

    @staticmethod
    def parallel(v1: float, v2: float) -> float:
        return v1 * v2 / (v1 + v2)
