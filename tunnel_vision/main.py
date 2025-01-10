""" The main running method of this program, takes an event tracking and a position tracking csv (each referring to
 the same game)

 This module will write a new csv file with the current game data.
 """

from event_builders.event_shifts import event_shifts
from event_builders.puck_loss import build_events
from tunnel_vision.open_passes import open_passes
import csv


def main(tracker_file: str, event_file: str, error_width: int, file_name: str) -> None:
    """Write a csv file that contains all the possible passes in a hockey game that could have been made before
    a player had lost the puck to the other team.

    error_width is the width (in feet) of where a puck can be shot in a teammates direction when verifying whether
    there are players on the opposite team able to intercept the pass.

    Preconditions:
    - tracker_file is a csv file with :
    Image Id,Period,Game Clock,Player or Puck,Team,Player Id,Rink Location X (Feet),Rink Location Y (Feet),
    Rink Location Z (Feet),Goal Score
    as column attributes

    - event_file is a csv file with :
    Date,Home_Team,Away_Team,Period,Clock,Home_Team_Skaters,Away_Team_Skaters,Home_Team_Goals,Away_Team_Goals,Team,
    Player_Id,Event,X_Coordinate,Y_Coordinate,Detail_1,Detail_2,Detail_3,Detail_4,Player_Id_2,X_Coordinate_2,
    Y_Coordinate_2
    as column attributes

    - error_width < 42
    """

    events = build_events(event_file)
    intermediate_data = open_passes(event_shifts(events, tracker_file), events, error_width)

    output_data = [["Event", "Team", "Player in Possession", "Teammate to Pass to", "Seconds Left", "Period"]]

    for event in intermediate_data:
        for miss in intermediate_data[event]:
            result = [str(event)] + miss
            output_data.append(result)

    with open(f"{file_name}.csv", mode="w", newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerows(output_data)
