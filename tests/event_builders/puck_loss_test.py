"""Tests for puck_loss event builder"""

from event_builders.puck_loss import build_events
from resources.sample_data import gh_events


def test_build_events_with_gh():

    events = build_events(gh_events)

    assert len(events) > 0
