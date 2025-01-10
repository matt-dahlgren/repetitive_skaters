"""This module contains the functions to find open passes before Takeaways occur for players during an event"""

from entities.player import Player
from entities.event import Event
from entities.player_cones import PlayerCones
from entities.hockey_rink_constants import AWAY, HOME


def open_passes(players: dict[int, list[Player]], events: dict[int, Event], width: int) -> (
        dict)[int, list[list[str]]]:
    """Return a dictionary that maps each event to a list of passes that are 'open'.
    A shot is open if within an isosceles triangle (with the player in possession of the puck being the tip and
    a player on the same team being the centre of the base with some width) there is no net, or player on the opposite
    team within that area.

    Since a player cannot immediately pass a puck to a teammate this function will take the player in possession's
    current position at any point and verify locations of teammates or players on the opposite team after one second
    of play.

    Pre-Conditions:
        - players: keys correspond to events, whereas its values are list of players in that event.
        - events: keys correspond to events, whereas its values contains the information to that event number.
        - width: the width of the margin for error of a shot to a teammate

    The returning dictionary's keys refer to the event number and its values are a list of possible shots that could
    have been made. In the format of: player's team, player in possession of the puck's number, the open teammate's
    number, and the time of play, the period.
    """

    result = {}
    for event in players:

        if event not in result:

            result[event] = []

        period = events[event].get_period()

        for time in range(events[event].get_pickup(), events[event].get_takeaway(), -1):

            player_lost = events[event].get_player_lost()

            team = events[event].get_team()
            if team == AWAY:
                other_team = HOME

            else:
                other_team = AWAY

            ice_data = clean_ice_data(players[event], player_lost, time)

            open_pass = find_empty_cones(ice_data[team], ice_data[other_team], player_lost, team, width, time, period)

            if open_pass not in result[event] and open_pass != []:

                for miss in open_pass:
                    result[event].append(miss)

    return result


def clean_ice_data(on_ice: list[Player], player_in_possession: int, time: int) -> dict[int, list[Player]]:
    """Map teams to their respective players who have positions after one second of player, excluding the player
    who currently has the puck, their position will be set at time.

    Then further appropriates data for use by modifying the result with get_post_second_position.
    """

    players_on_ice = {HOME: [], AWAY: []}

    # in case there is no data in the input, return an empty result without iterating further
    if not on_ice:
        return players_on_ice

    for player in on_ice:

        if player.get_number() != player_in_possession and player.has_next_second(time):

            players_on_ice[player.get_team()].append(player)

        if player.get_number() == player_in_possession:

            players_on_ice[player.get_team()].append(player)

    return players_on_ice


def find_empty_cones(friendly_team: list[Player], unfriendly_team: list[Player], possession: int,
                     team: int, width: int, time: int, period: int) -> list[list[str]]:
    """Finds empty cones in this time slot if any and return a list of tuples containing the team of the player in
    positions, the player_number and """

    result = []

    if team == AWAY:
        team_string = 'Away'

    else:
        team_string = 'Home'

    # verify that the player in possession is in fact in on_ice
    player_in_possession = None

    for player in friendly_team:
        if player.get_number() == possession:
            player_in_possession = player

    # return an empty list in case the player is either found twice or found no times in this list
    if player_in_possession is None:
        return result

    for teammate in friendly_team:

        if (teammate == player_in_possession or not teammate.has_next_second(time) or not
                player_in_possession.has_time(time)):
            continue

        possible_pass = PlayerCones(player_in_possession, teammate, width, time)

        if possible_pass.is_empty(collect_unfriendly_coords(unfriendly_team, time)):

            event = (team_string, str(possession), str(possible_pass.get_player_2()), seconds_to_minutes(time),
                     str(period))
            event = list(event)

            if event not in result and teammate.get_number() != player_in_possession.get_number():
                result.append(event)

    return result


def collect_unfriendly_coords(enemy_team: list[Player], time) -> list[tuple[float, float]]:
    """Collects the coordinates of the players on the opposite team after a second from time"""

    result = []
    for player in enemy_team:

        if player.has_next_second(time):
            result.append(player.get_next_second(time))

    return result


def seconds_to_minutes(seconds: int) -> str:
    """Convert time in seconds to a string form of minutes similar to clock time"""

    minutes = seconds // 60
    seconds = seconds - minutes * 60

    if seconds < 10:
        return f"{minutes:02d}:0{seconds:}"

    return f"{minutes:02d}:{seconds:}"
