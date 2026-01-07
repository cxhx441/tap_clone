from __future__ import annotations
import math
import abc

class OctaveBands:
    def __init__(self, data=None):
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

        if data is not None:
            self._apply_input_data(data)

    def _apply_input_data(self, data):
        if len(data) == 8:
            for key, num in zip(self.ob.keys(), data):
                if num < 0:
                    raise ValueError("No negative values")
                self.ob[key] = num
        elif len(data) == 1:
            if data[0] < 0:
                raise ValueError("No negative values")
            for key in self.ob.keys():
                self.ob[key] = data[0]
        else:
            raise ValueError("Octave_Band takes data list of length 1, 8, or None")


    def noise_criteria(self) -> tuple[float, int]:
        """ TODO Return NC and offending octave band frequency. """
        return 0, 0

    def dBA(self) -> float:
        """ TODO Return dBA value. """
        return 0

    def linear_addition(self, other: OctaveBands) -> OctaveBands:
        """ Returns an OB object with the linear addition of a and b. """
        c = OctaveBands()
        for key in c.ob.keys():
            c.ob[key] = self.ob[key] + other.ob[key]
        return c

    def decibel_addition(self, other: OctaveBands) -> OctaveBands:
        """ Returns an OB object with the decibel addition of a and b. """
        c = OctaveBands()
        for key, av, bv in zip(c.ob.keys(), self.ob.values(), other.ob.values()):
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
        for key in c.ob.keys():
            c.ob[key] = max(0, self.ob[key] - other.ob[key])
        return c


class Node:
    def __init__(self, title=""):
        self.title = title
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
        self.ob = OctaveBands(obdata)


class Straight_Duct(Node):
    def __init__(self, h, w, l, liner, title=""):
        super().__init__(title)
        self.h = h
        self.w = w
        self.l = l
        self.liner = liner

    def ob_atten(self):
        """ TODO lookup table for h/w/liner combo """
        return OctaveBands()


class Elbow_Duct(Node):
    def __init__(self, h, w, l, liner, vertical:bool, title=""):
        super().__init__(title)
        self.h = h
        self.w = w
        self.l = l
        self.vertical = vertical
        self.liner = liner

    def ob_regen(self):
        """ TODO lookup table for CFM vs size etc."""
        dim = self.h if self.vertical else self.w
        return OctaveBands()

    def ob_atten(self):
        """ TODO lookup table for h/w/liner combo """
        dim = self.h if self.vertical else self.w
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
