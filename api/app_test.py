from app import process_query


def test_knows_about_dinosaurs():

    assert process_query("dinosaurs") == "Dinosaurs ruled the \
Earth 200 million years ago"


def test_knows_team_name():

    assert process_query("What is your name?") == "team"


def test_does_not_know_about_asteroids():

    assert process_query("asteroids") == "Unknown"


def test_minus():

    assert process_query("What is 30 minus 25?") == "5"


def test_mutiply():

    assert process_query("What is 2 multiplied 25?") == "50"
