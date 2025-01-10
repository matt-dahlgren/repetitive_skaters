"""Test whether the csv file built in main is constructed properly"""

from tunnel_vision.main import main

from resources.sample_data import gh_events, gh_tracking


def test_main():
    """Test the main function and print out the resulting csv row by row"""

    main(gh_tracking, gh_events, 1, "output_data")
