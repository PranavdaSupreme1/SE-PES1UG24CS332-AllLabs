import re
from hypothesis import given, settings, strategies as st
from traffic_fine import parse_ticket_id, total_fines, speed_excess

# ---------- 1. "No crash" fuzz tests (text, None, and other junk types) ----------
junk = st.text() | st.none() | st.integers() | st.binary() | st.lists(st.integers())


@given(junk)
def test_parse_ticket_id_no_crash(s):
    try:
        parse_ticket_id(s)
    except Exception as e:
        assert False, f"parse_ticket_id crashed with: {e!r} on input {s!r}"


@given(junk)
def test_total_fines_no_crash(s):
    try:
        total_fines(s)
    except Exception as e:
        assert False, f"total_fines crashed with: {e!r} on input {s!r}"


@given(junk)
def test_speed_excess_no_crash(s):
    try:
        speed_excess(s)
    except Exception as e:
        assert False, f"speed_excess crashed with: {e!r} on input {s!r}"


# ---------- 2. Property tests with structured, valid inputs ----------
@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=5),
       st.integers(0, 9999), st.integers(0, 10**6))
def test_parse_ticket_id_valid_roundtrip(prefix, year, serial):
    result = parse_ticket_id(f"{prefix}-{year}-{serial}")
    assert result == (prefix.upper(), year, serial)


@given(st.lists(st.integers(0, 5000), min_size=1, max_size=20))
def test_total_fines_valid_is_capped_sum(amounts):
    result = total_fines(",".join(map(str, amounts)))
    assert result == min(sum(amounts), 10000)
    assert 0 <= result <= 10000


@given(st.text())
def test_total_fines_result_never_exceeds_cap(s):
    result = total_fines(s)
    assert result is None or 0 <= result <= 10000


@given(st.integers(0, 400), st.integers(1, 400))
def test_speed_excess_valid(speed, limit):
    assert speed_excess(f"{speed}/{limit}") == (speed - limit) * 100 // limit


# ---------- 3. Specific edge cases the fuzzer found / we expect ----------
def test_known_bad_inputs_return_none():
    assert parse_ticket_id(None) is None
    assert parse_ticket_id("") is None
    assert parse_ticket_id("TF-2024") is None
    assert parse_ticket_id("TF-20x4-0456") is None
    assert parse_ticket_id("TF-2024-0456-9") is None
    assert total_fines(None) is None
    assert total_fines("500,,300") is None
    assert total_fines("500,abc") is None
    assert total_fines("-500,200") is None
    assert speed_excess(None) is None
    assert speed_excess("72/0") is None     # ZeroDivisionError before the fix
    assert speed_excess("72") is None
    assert speed_excess("a/b") is None


def test_known_good_inputs():
    assert parse_ticket_id("tf-2024-0456") == ("TF", 2024, 456)
    assert total_fines("500,1200,300") == 2000
    assert total_fines("9000,9000") == 10000
    assert speed_excess("72/60") == 20
