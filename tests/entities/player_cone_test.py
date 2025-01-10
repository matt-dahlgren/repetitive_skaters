"""This module tests the player cone entity"""

from entities.player import Player
from entities.player_cones import PlayerCones


def test_in_player_cone():
    """Test if some coordinate (that does fall within the cone) is within a player cone"""

    player_1 = Player("1", 2)
    player_2 = Player("2", 3)

    coord_1 = 65.670, 0
    coord_2 = -65.670, 0
    test_coord = -64.056, 0.089

    player_1.set_position_at(800, coord_1)
    player_2.set_position_at(799, coord_2)

    test_cone = PlayerCones(player_1, player_2, 2, 800)

    assert test_cone.contains_coordinate(test_coord)


def test_in_player_cone_with_invalid_coordinates():
    """Test that a coordinate outside a player cone returns false"""

    player_1 = Player("1", 2)
    player_2 = Player("2", 3)

    coord_1 = 65.670, 0
    coord_2 = -65.670, 0
    test_coord = 0.0, -35.654

    player_1.set_position_at(800, coord_1)
    player_2.set_position_at(799, coord_2)

    test_cone = PlayerCones(player_1, player_2, 2, 800)

    assert not test_cone.contains_coordinate(test_coord)
