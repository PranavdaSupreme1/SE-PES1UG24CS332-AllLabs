"""Line/code coverage tests for traffic_fine.py."""
import pytest
from traffic_fine import speeding_fine, license_action, total_penalty


@pytest.mark.parametrize(
    "speed, limit, zone, expected",
    [
        (50, 60, "city", 0),          # speed at/below limit
        (61, 60, "school", 2000),     # school base, ordinary excess
        (61, 60, "highway", 1000),    # highway base
        (61, 60, "city", 500),        # other-zone base
        (81, 60, "city", 1000),       # excess > 20
        (101, 60, "school", 6000),    # excess > 40
    ],
)
def test_speeding_fine_cases(speed, limit, zone, expected):
    assert speeding_fine(speed, limit, zone) == expected


@pytest.mark.parametrize(
    "points, commercial, repeat, expected",
    [
        (2, False, False, "none"),
        (4, False, False, "notice"),
        (8, False, False, "warning"),
        (8, False, True, "suspend"),
        (12, False, False, "suspend"),
        (12, True, False, "revoke"),
    ],
)
def test_license_action_cases(points, commercial, repeat, expected):
    assert license_action(points, commercial, repeat) == expected


def test_total_penalty_under_cap():
    assert total_penalty([100, 200, 300]) == 600


def test_total_penalty_capped():
    assert total_penalty([6000, 6000]) == 10000


def test_total_penalty_rejects_negative():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([100, -1])
