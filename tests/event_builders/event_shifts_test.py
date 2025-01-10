"""Tests that event_shifts builds correctly"""

from resources.sample_data import gh_events, gh_tracking
from event_builders.puck_loss import build_events
from event_builders.event_shifts import event_shifts


def test_event_shifts_with_gh():
    """Tests that event_shifts builds correctly"""
    tracking = event_shifts(build_events(gh_events), gh_tracking)

    assert len(tracking) > 0


def test_event_shifts_equal_puck_loss_len_with_gh():
    """Tests that the event_shifts is the same length as the puck loss dictionary"""

    puck_loss_dict = build_events(gh_events)
    tracking = event_shifts(puck_loss_dict, gh_tracking)

    assert len(puck_loss_dict) == len(tracking)


def test_event_shifts_with_empty_input():
    """Tests that event_shifts builds an empty dictionary when no events are provided"""
    tracking = event_shifts({}, gh_tracking)

    assert len(tracking) == 0
