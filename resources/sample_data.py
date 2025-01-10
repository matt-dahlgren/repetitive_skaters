# In this file we have sample data from three separate games.
#
# Tracking updates the x,y coordinates of a player and puck whose x denotes their location on the long side of a hockey
# rink (between -100 and 100 with 0 being at the centre), and whose y coordinate denotes their position on the short
# side of the rink (between -42.5 and 42.5). Each of these are in feet since a hockey rink is 200ft x 85ft.
#
# Events track actions that are taken in a hockey game. In this project we will be focusing on the puck recovery event
# (when a player gains possession of the puck) and the incomplete play event (when a player loses possession of the
# puck to the other team).

# Team G at Team H

gh_tracking = \
    "https://github.com/bigdatacup/Big-Data-Cup-2025/releases/download/Data/2024-10-25.Team.H.@.Team.G.-.Tracking.csv"

gh_events = \
    "https://github.com/bigdatacup/Big-Data-Cup-2025/releases/download/Data/2024-10-25.Team.H.@.Team.G.-.Events.csv"

# Team D at Team C

dc_tracking = \
    "https://github.com/bigdatacup/Big-Data-Cup-2025/releases/download/Data/2024-11-15.Team.D.@.Team.C.-.Tracking.csv"

dc_events = \
    "https://github.com/bigdatacup/Big-Data-Cup-2025/releases/download/Data/2024-11-15.Team.D.@.Team.C.-.Events.csv"

# Team F at Team E

fe_tracking = \
    "https://github.com/bigdatacup/Big-Data-Cup-2025/releases/download/Data/2024-11-16.Team.F.@.Team.E.-.Tracking.csv"

fe_events = \
    "https://github.com/bigdatacup/Big-Data-Cup-2025/releases/download/Data/2024-11-16.Team.F.@.Team.E.-.Events.csv"
