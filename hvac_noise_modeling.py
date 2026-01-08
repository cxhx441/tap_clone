from __future__ import annotations
from typing import Optional, Union
import math

class OctaveBands:
    def __init__(self, data: Union[list[float], float] = 0):
        self.ob = {
            63: 0,
            125: 0,
            250: 0,
            500: 0,
            1000: 0,
            2000: 0,
            4000: 0,
            8000: 0,
            }

        if isinstance(data, list):
            if len(data) != 8:
                raise ValueError("Octave_Band takes data list of length 1, 8, or None")
            for key, num in zip(self.ob, data):
                if num < 0:
                    self.ob[key] = num
        elif isinstance(data, float):
            for key in self.ob:
                self.ob[key] = data[0]
        else:
            raise TypeError("data arg must be float or list (of len 8)")

    def reset(self):
        for key in self.ob:
            self.ob[key] = 0

    def noise_criteria(self) -> tuple[float, int]:
        """ TODO Return NC and offending octave band frequency. """
        return 0, 0

    def dBA(self) -> float:
        """ TODO Return dBA value. """
        return 0

    def linear_addition(self, other: OctaveBands) -> OctaveBands:
        """ Returns an OB object with the linear addition of a and b. """
        c = OctaveBands()
        for key in c.ob:
            c.ob[key] = self.ob[key] + other.ob[key]
        return c

    def decibel_addition(self, other: OctaveBands) -> OctaveBands:
        """ Returns an OB object with the decibel addition of a and b. """
        c = OctaveBands()
        for key, av, bv in zip(c.ob, self.ob.values(), other.ob.values()):
            self_intensity = 10**(av / 10) if av >= 0 else 0
            other_intensity = 10**(bv / 10) if bv >= 0 else 0
            c.ob[key] = 10*math.log10(self_intensity + other_intensity)
        return c

    def linear_subtraction(self, other: OctaveBands) -> OctaveBands:
        """
        Returns an OB object with the linear subtraction equivalent to a - b.
        No negatives.
        """
        c = OctaveBands()
        for key in c.ob:
            c.ob[key] = max(0, self.ob[key] - other.ob[key])
        return c



class Node:
    def __init__(self, title=""):
        self.title = title
        self.input_nodes = set()
        self.output_nodes = set()
        self.ob_input = OctaveBands()

    def ob_regen(self):
        return OctaveBands()

    def ob_atten(self):
        return OctaveBands()

    def ob_output(self):
        a, b, c = self.ob_input, self.ob_regen(), self.ob_atten()
        input_plus_regen = OctaveBands.linear_addition(a, b)
        return OctaveBands.linear_subtraction(input_plus_regen, c)


class Source(Node):
    def __init__(self, obdata, title=""):
        super().__init__(title)
        self.levels = OctaveBands(obdata)


class StraightDuct(Node):
    def __init__(self, h, w, l, liner, title=""):
        super().__init__(title)
        self.h = h
        self.w = w
        self.l = l
        self.liner = liner

    def ob_atten(self):
        """ TODO lookup table for h/w/liner combo """
        return OctaveBands()


class ElbowDuct(Node):
    def __init__(self, h, w, liner, vertical:bool, title=""):
        super().__init__(title)
        self.h = h
        self.w = w
        self.vertical = vertical
        self.liner = liner

    def ob_regen(self):
        """ TODO lookup table for CFM vs size etc."""
        bend_dimension = self.h if self.vertical else self.w
        return OctaveBands()

    def ob_atten(self):
        """ TODO lookup table for h/w/liner combo """
        bend_dimension = self.h if self.vertical else self.w
        return OctaveBands()


class FreeFieldReceiver(Node):
    def __init__(self, r, q, title=""):
        super().__init__(title)
        self.r = r
        self.q = q

    def ob_atten(self):
        return OctaveBands( [10 * math.log10(
            ( 4 * math.pi * self.r**2 ) / self.q
            )]
        )

# class Receiver(Node):
#     def __init__(self, h, w, l, alpha_prop, title=""):
#         super().__init__(title)
#         self.h = h
#         self.w = w
#         self.l = l
#         self.alpha_prop = alpha_prop

#     def ob_atten(self):
#         """ TODO lookup table for h/w/liner combo """
#         return OctaveBands()

class Path:
    def __init__(self):
        self.head = Node("head")

    def check_for_cycles(self):
        """ TODO """
        pass

    def crunch_calcs(self):
        """ TODO """
        pass

    def print_report(self):
        """ TODO """
        pass

