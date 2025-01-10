# This file contains the documentation for the object that represents a player in a hockey game.

class Player:
    """ A hockey player

    Attributes:
        - number: The player's jersey number, -1 iff the player's number is not registered in the input data.
        - positions: The player's coordinates in feet from centre ice at a given time. The player's coordinates are
        taken multiple times per second, the list mapped from the time the player's on the ice will be in order from
        the earliest instance of that second to latest instance of the second.
        - team: Whether the player is on the home or away team. 0 refers to the home team, and 1 refers to the away
        team.

    Representation Invariants:
        - positions: the players' coordinates at any and all times are: -100 <= x <= 100 and -42.5 <= y <= 42.5.
    """

    _number: int
    _positions: dict[int, tuple[float, float]]
    _team: int

    def __init__(self, number: str, team: int) -> None:
        # both of these attributes will be updated when reading a game.
        self._positions = {}
        self._team = team

        # get the player's number, if there is no number provided set as -1
        if number == "":
            self._number = -1
        else:
            self._number = int(number)

    def get_position(self, time: int) -> tuple[float, float]:
        """Return the first coordinate at time of this player"""

        return self._positions[time]

    def set_position_at(self, time: int, position: tuple[float, float]) -> None:
        """Set the position of this player at time"""

        self._positions[time] = position

    def time_recorded(self, time: int) -> bool:
        """Return True iff time is already in self._positions"""

        return time in self._positions

    def get_number(self) -> int:
        """Return the number of this player's jersey"""

        return self._number

    def has_next_second(self, time: int) -> bool:
        """Return True iff the player has a position in the next second"""

        for second in self._positions:
            if second == time - 1:
                return True

        return False

    def get_next_second(self, time: int) -> tuple[float, float]:
        """Get the player's position at the next second of play from time

        Pre-Condition:
            - self.has_next_second() == True
        """

        return self._positions[time - 1]

    def get_team(self) -> int:
        """Return this player's team number"""

        return self._team

    def has_time(self, time: int) -> bool:
        """Return True iff the player has a coordinate at this time"""

        for coord in self._positions:
            if coord == time:
                return True

        return False
