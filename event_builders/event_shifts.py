"""This file builds the on ice positions of players from a dictionary of ordered events"""

import io
import csv
import requests

from entities.event import Event
from entities.player import Player
from entities.hockey_rink_constants import AWAY, HOME
from event_builders.puck_loss import minutes_to_seconds

# column constants for a tracking csv file
PERIOD = 1
TIME = 2
TRACK_TYPE = 3
TEAM = 4
PLAYER = 5
X_COORD = 6
Y_COORD = 7

# index constants for event_information return
EVENT_TEAM = 0
EVENT_PLAYER = 1
EVENT_PERIOD = 2
EVENT_START = 3
EVENT_END = 4


def event_shifts(events: dict[int: Event], tracking_file: str) -> dict[int, list[Player]]:
    """Using the event durations from an ordered dictionary of events built from the corresponding event file to
    tracking_file, build a dictionary mapping each event number to a dictionary that maps each player on the ice
    to their coordinates on the ice per second through the play.

    If a player is not on the ice for the entire play they will not be in the result of this function
    """

    result = {}

    if events == {}:
        return result

    response = requests.get(tracking_file)

    if response.status_code == 200:

        tracking_data = response.text
        tracking_reader = csv.reader(io.StringIO(tracking_data), delimiter=',')
        row_counter = 0

        for row in tracking_reader:

            if row_counter == 0:
                row_counter += 1
                continue

            modify_player_coords(result, row, events)

            row_counter += 1

    return result


def modify_player_coords(events_to_players: dict[int, list[Player]], row: list[str], events: dict[int, Event]) -> None:
    """Check if each event needs to be modified with this row's data, if so, then modify"""

    # if this row refers to the goalie or a puck, return early
    if row[PLAYER] == "Go" or row[TRACK_TYPE] == "Puck":
        return

    time = minutes_to_seconds(row[TIME])
    period = int(row[PERIOD])

    for event in events:
        if events[event].in_event(period, time):
            build_event_shift(row, events_to_players, event)


def build_event_shift(row: list[str], current_shifts: dict[int, list[Player]], event_number: int) -> None:
    """Updates a dictionary by adding a new Player to the event if they do not already appear in that event
    and only updates the player's position if it has not been recorded for that time yet"""

    player_count = 0
    time = minutes_to_seconds(row[TIME])

    if row[X_COORD] == '' or row[Y_COORD] == '':
        return

    coords = float(row[X_COORD]), float(row[Y_COORD])

    # check if this event has been added to current_shifts yet
    if event_number in current_shifts:

        # check if player is already added for this event
        for player in current_shifts[event_number]:

            if row[PLAYER] == "":

                player_count += 1
                continue

            if int(row[PLAYER]) == player.get_number() and not player.time_recorded(time):
                current_shifts[event_number][player_count].set_position_at(time, coords)

                # modify input and return early
                return

            player_count += 1

    else:
        current_shifts[event_number] = []

    # the player has not yet been added to the list of this event, check what team they're on, initialize a new player
    # and modify input
    if row[TEAM] == "Home":
        player_team = HOME

    else:
        player_team = AWAY

    new_player = Player((row[PLAYER]), player_team)
    new_player.set_position_at(time, coords)
    current_shifts[event_number].append(new_player)
