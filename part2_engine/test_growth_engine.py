from part2_engine.growth_engine import mom_growth, is_flagged, validate_feed


def test_ethnic_wear_april_to_may():
    # GIVEN
    previous = 104520.77
    current = 185107.61

    # WHEN
    growth = mom_growth(previous, current)
    result = is_flagged(growth)

    # THEN
    assert growth == 77.1
    assert result == "flagged"


def test_beauty_may_to_june():
    # GIVEN
    previous = 35542.11
    current = 37559.07

    # WHEN
    growth = mom_growth(previous, current)
    result = is_flagged(growth)

    # THEN
    assert growth == 5.67
    assert result == "not_flagged"


def test_exact_boundary():
    # GIVEN
    previous = 100000
    current = 108000

    # WHEN
    growth = mom_growth(previous, current)
    result = is_flagged(growth)

    # THEN
    assert growth == 8.0
    assert result == "escalate_exact_boundary"


def test_corrupted_feed():
    # GIVEN
    csv_path = "part2_engine/fixtures/corrupted_feed.csv"

    # WHEN
    valid, errors = validate_feed(csv_path)

    # THEN
    assert valid is False

    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]