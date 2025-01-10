"""Tests that open_passes builds correctly."""

from tunnel_vision.open_passes import open_passes, clean_ice_data
from event_builders.event_shifts import event_shifts
from event_builders.puck_loss import build_events
from entities.hockey_rink_constants import HOME, AWAY

from resources.sample_data import gh_events, gh_tracking


def test_open_passes_with_gh():
    """Tests that open_passes builds with gh game"""

    puck_loss_dict = build_events(gh_events)
    tracking = event_shifts(puck_loss_dict, gh_tracking)

    events = open_passes(tracking, puck_loss_dict, 1)

    assert len(events) > 0


def test_open_passes_with_empty_dictionaries():
    """Test that open_passes builds an empty returning dictionary with empty inputs"""

    events = open_passes({}, {}, 1)

    assert len(events) == 0


def test_clean_ice_data_with_empty_dictionaries():
    """Test that open_passes builds an empty returning dictionary with empty inputs"""

    on_ice = clean_ice_data([], 1, 1)

    assert on_ice == {HOME: [], AWAY: []}
