"""This module contains the Event class."""


class Event:
    """This class represents the data held by an event being tracked by this program

    A notable event has a player hold the puck for at least 3 seconds which leads to a Takeaway from the other team.

    Attributes:
        - team_lost: the team that lost possession of the puck.
        - player_lost: the player id that lost possession of the puck.
        - pickup: the time that the player_lost attains possession of the puck.
        - takeaway: the time that the player_lost loses possession of the puck.
        - period: the period of the game this event occurs in.

    Representation Invariants:

        - pickup >= takeaway + 3
    """

    _team_lost: int
    _player_lost: int
    _pickup: int
    _takeaway: int
    _period: int

    def __init__(self, team_lost: int, pickup: int, takeaway: int, player_lost: int, period: int) -> None:

        self._team_lost = team_lost
        self._player_lost = player_lost
        self._pickup = pickup
        self._takeaway = takeaway
        self._period = period

    def get_player_lost(self) -> int:
        """Get the team the player that lost the puck and the player id of the player that lost the puck"""

        return self._player_lost

    def get_period(self) -> int:
        """Return the period that this event occurs"""

        return self._period

    def get_pickup(self) -> int:
        """Return when the player attains the puck"""

        return self._pickup

    def get_takeaway(self) -> int:
        """Return when the player loses the puck to the other team"""

        return self._takeaway

    def get_team(self):
        """Return the team the player that lost the puck was on."""

        return self._team_lost

    def in_event(self, period: int, time: int) -> bool:
        """Check if time occurs in this event"""

        return self._pickup >= time >= self._takeaway and self._period == period
