# this file contains the documentation for the player cone class which makes a triangle from a player to another.
# this triangle represents a shot a player can make to another to pass the puck

from entities.player import Player
from entities.hockey_rink_constants import WEST_NET_POSITION, EAST_NET_POSITION
from numpy import sqrt, floor


class PlayerCones:
    """ A cone made between two Players

    Attributes:
        - player1: the player that this line is originating from.
        - player2: the player that this line is extending to.
        - width: the width in feet of the width of the cone between player1 and player2, with the wide side being having
        player2 on it.
        - length: the length (rounded to the highest integer) in feet of the line between player1 and player2.
        - time: the time that this line is initialized at (in seconds from the end of a period).
        - centre: the centre of the line between the two players, rounded to 3 decimal places.

    Representation Invariants:
        - player1 is in play at time.
        - player2 is in play at time.
        - abs(width) <= 42.5
    """
    _player1: Player
    _player2: Player
    _width: int
    _length: int
    _centre: tuple[float, float]
    _time: int
    _area: float

    def __init__(self, player1: Player, player2: Player, width: int, time: int):
        self._player1 = player1
        self._player2 = player2
        self._width = width
        self._time = time

        player1_pos = player1.get_position(time)
        player2_pos = player2.get_next_second(time)

        # the length of a straight line starting at player1 ending at player 2
        self._length = abs(sqrt((player1_pos[0] - player2_pos[0]) ** 2 + (player1_pos[1] - player2_pos[1]) ** 2)) + 1

        self._centre = (round_to_three_decimals((player1_pos[0] + player2_pos[0]) / 2),
                        round_to_three_decimals((player1_pos[1] + player2_pos[1]) / 2))

        self._area = triangle_area(player1_pos, bounded_addition(player2_pos, width, 1, 1),
                                   bounded_addition(player2_pos, width, 0, 0))

    def contains_coordinate(self, position: tuple[float, float]) -> bool:
        """Determine whether a set of coordinates is contained within this line.

        Pre-Condition:
            - position refers to the position of neither player1 nor player2.
            - position's coordinates are: -100 <= x <= 100 and -42.5 <= y <= 42.5
        """

        # point a is the position of player one
        point_a = self._player1.get_position(self._time)

        # points b and c are the vertices of this cone
        player2_pos = self._player2.get_position(self._time - 1)
        point_b = bounded_addition(player2_pos, self._width, 1, 1)
        point_c = bounded_addition(player2_pos, self._width, 0, 0)

        position_triangle = (triangle_area(point_a, point_b, position) + triangle_area(point_a, position, point_c)
                             + triangle_area(point_b, position, point_c))

        if self._area == position_triangle:
            return True

        return False

    def is_empty(self, on_ice_positions: list[tuple[float, float]]) -> bool:
        """ Checks if any of the positions in on_ice_positions fall within this cone or if there are any nets in
        the cone.
        """

        for position in on_ice_positions:
            if self.contains_coordinate(position):
                return False

        if self.contains_coordinate(WEST_NET_POSITION) or self.contains_coordinate(EAST_NET_POSITION):
            return False

        return True

    def get_player_2(self) -> int:
        """Returns the number of player_2"""

        return self._player2.get_number()


def round_to_three_decimals(value: float) -> float:
    """Rounds value to three decimal points"""

    # prepare and integer to be removed from value to have the end result be a zero followed by trailing decimal points.
    integer = int(value)
    three_decimals = round(value - integer, 3)

    return integer + three_decimals


def triangle_area(point_a: tuple[float, float], point_b: tuple[float, float], point_c: tuple[float, float]) -> int:
    """Calculate the area of a triangle with coordinates point_a, point_b and point_c as vertices

    An area for error allows for a player to be slightly outside the triangle to get an integer response since float
    division is not overly reliable.
    """

    return floor(abs(point_a[0] * (point_b[1] - point_c[1]) + point_b[0] * (point_c[1] - point_a[1]) +
                     point_c[0] * (point_a[1] - point_b[1])))


def bounded_addition(end_point: tuple[float, float], width: int, x_direction: int,
                     y_direction: int) -> tuple[float, float]:
    """Returns the position after incrementation of a coordinate in accordance to the length and width of this line

    Pre-Condition:
        - x_direction is either 0 or 1.
        - y_direction is either 0 or 1.
    """

    end_of_line = end_point

    # we find the adjustment factor to find the end of the vision cone. We know the hypotenuse from the centre of
    # the cone (where player2 stands) to the end of the cone is half the width of our cone, thus the adjustment of
    # a coordinate will be corresponding to a and b in the pythagorean thm (but a and b are equal)
    shift_factor = round_to_three_decimals((sqrt(2) * width) / 4)

    # the min and max functions assure that the returned coordinate is within
    if x_direction == 1:
        x_coord = min(end_of_line[0] + shift_factor, 100)

    else:
        x_coord = max(end_of_line[0] - shift_factor, -100)

    if y_direction == 1:
        y_coord = min(end_of_line[1] + shift_factor, 42.5)

    else:
        y_coord = max(end_of_line[1] - shift_factor, -42.5)

    return x_coord, y_coord
