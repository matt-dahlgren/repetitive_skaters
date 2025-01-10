"""this file builds a directory of puck possessions that lasted at least 4 seconds and result in a change of possession
to the other team.
"""

import csv
import requests
import io

from entities.hockey_rink_constants import AWAY, HOME
from entities.event import Event

# constants that can be changed determined on how the user's input data is setup
LINE_INDICES = {1: "home_team", 3: "period", 4: "time", 9: "team", 10: "player", 11: "event_type", 18: "player_pickup"}

HOME_TEAM = 1
PERIOD = 3
TIME = 4
TEAM = 9
PLAYER = 10
EVENT_TYPE = 11
PLAYER_PICKUP = 18

# event types
PASS = "Play"
PUCK_RECOVERY = "Puck Recovery"
PUCK_LOSS = "Takeaway"


def build_events(event_file: str) -> dict[int, Event]:
    """Build a dictionary that firstly maps the team to a dictionary containing times mapped to events

    Precondition:
        - event_file is a link to a csv file with columns:
        Date,Home_Team,Away_Team,Period,Clock,Home_Team_Skaters,Away_Team_Skaters,Home_Team_Goals,Away_Team_Goals,Team,
        Player_Id,Event,X_Coordinate,Y_Coordinate,Detail_1,Detail_2,Detail_3,Detail_4,Player_Id_2,
        X_Coordinate_2,Y_Coordinate_2
    """

    result = {}
    event_counter = 1

    # initialize to comparable values that will return false upon further lines of this while loop
    last_pickup = ("-1", "21:00", "-1")
    home_team = ""
    response = requests.get(event_file)

    if response.status_code == 200:

        event_data = response.text
        event_reader = csv.reader(io.StringIO(event_data), delimiter=',')
        row_counter = 0
        for row in event_reader:

            if row_counter == 1:
                home_team = row[1]

            elif row_counter >= 1 and row[EVENT_TYPE] == PASS:
                last_pickup = row[TEAM], row[TIME], row[PLAYER_PICKUP]

            elif row_counter >= 1 and row[EVENT_TYPE] == PUCK_RECOVERY:
                last_pickup = row[TEAM], row[TIME], row[PLAYER]

            elif row_counter >= 1 and row[EVENT_TYPE] == PUCK_LOSS:

                play_start = minutes_to_seconds(last_pickup[1])
                timestamp = minutes_to_seconds(row[TIME])
                play_duration = play_start - timestamp

                if last_pickup[0] == home_team and play_duration > 2:

                    result[event_counter] = Event(HOME, play_start, timestamp, int(float(last_pickup[2])),
                                                  int(float(row[PERIOD])))

                    event_counter += 1

                elif last_pickup[0] != home_team and play_duration > 2:

                    result[event_counter] = Event(AWAY, play_start, timestamp, int(float(last_pickup[2])),
                                                  int(float(row[PERIOD])))

                    event_counter += 1

                last_pickup = "-1", "21:00", "-1"

            row_counter += 1

    else:

        print(f"could not get data: {response.status_code}")

    return result


def minutes_to_seconds(minutes_left: str) -> int:
    """Convert the minutes : seconds of the event time from the time remaining in a period to seconds left in the
    period, if the time given is not a valid time return -1.

    >>> minutes_to_seconds("20:00")
    1200
    >>> minutes_to_seconds("21:00")
    -1
    """

    if minutes_left == "":
        return -1
    
    colon_index = minutes_left.index(":")
    minutes = int(minutes_left[:colon_index])
    seconds = int(minutes_left[colon_index + 1:])

    if minutes < 0 or minutes > 20 or seconds < 0 or seconds > 59 or (minutes == 20 and seconds != 0):
        return -1

    return 60 * minutes + seconds
