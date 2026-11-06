"""Branch coverage tests for every decision outcome in traffic_fine.py."""
import pytest
from traffic_fine import speeding_fine, license_action, total_penalty


# speeding_fine: speed limit, each zone selection, and both excess thresholds
@pytest.mark.parametrize(
    "speed, limit, zone, expected",
    [
        (60, 60, "school", 0),         # speed <= limit: True
        (61, 60, "school", 2000),      # speed <= limit: False; school
        (61, 60, "highway", 1000),     # highway
        (61, 60, "residential", 500),  # fallback zone
        (101, 60, "city", 1500),       # excess > 40: True
        (81, 60, "city", 1000),        # >40 False, >20 True
        (80, 60, "city", 1000),        # exact excess 20 -> base*2? see next case
        (70, 60, "city", 500),         # >40 False, >20 False
    ],
)
def test_speeding_fine_all_branches(speed, limit, zone, expected):
    # At excess 20, the function's >20 condition is False, so base is returned.
    if (speed, limit) == (80, 60):
        expected = 500
    assert speeding_fine(speed, limit, zone) == expected


# license_action: points thresholds, commercial and repeat-offender decisions
@pytest.mark.parametrize(
    "points, commercial, repeat, expected",
    [
        (12, True, False, "revoke"),    # >=12 true; commercial true
        (12, False, False, "suspend"),  # >=12 true; commercial false
        (11, False, True, "suspend"),   # >=12 false; >=8 true; repeat true
        (8, False, False, "warning"),  # repeat false
        (7, False, False, "notice"),   # >=8 false; >=4 true
        (3, True, True, "none"),       # >=4 false
    ],
)
def test_license_action_all_branches(points, commercial, repeat, expected):
    assert license_action(points, commercial, repeat) == expected


# total_penalty: empty/non-empty loop, negative-value exception, and cap decision
def test_total_penalty_empty_list():
    assert total_penalty([]) == 0


def test_total_penalty_normal_total():
    assert total_penalty([100, 250]) == 350


def test_total_penalty_negative_value_branch():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([100, -5])


def test_total_penalty_cap_branch():
    assert total_penalty([7000, 5000]) == 10000
