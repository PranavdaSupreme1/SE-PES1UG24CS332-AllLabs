import re

MAX_FINE_TOTAL = 10000
MAX_DIGITS = 9  # prevents huge-int DoS and int() digit-limit ValueError

# ASCII-only digits (int() would otherwise accept Unicode digits, '1_0', ' 5 ', '+5' ...)
_NUM = re.compile(r"[0-9]{1,%d}" % MAX_DIGITS)
_PREFIX = re.compile(r"[A-Za-z]{1,10}")


def _num(text):
    """Strict non-negative integer parse; returns None if invalid."""
    if isinstance(text, str) and _NUM.fullmatch(text):
        return int(text)
    return None


def parse_ticket_id(ticket_id):
    """Parse 'PREFIX-YEAR-SERIAL'. Returns (PREFIX, year, serial) or None if invalid."""
    if not isinstance(ticket_id, str):
        return None
    parts = ticket_id.split('-')
    if len(parts) != 3:
        return None
    prefix, year, serial = parts
    if not _PREFIX.fullmatch(prefix):
        return None
    year, serial = _num(year), _num(serial)
    if year is None or serial is None:
        return None
    return prefix.upper(), year, serial


def total_fines(amounts_csv):
    """Sum comma-separated fines, capped at 10000. Returns None if invalid."""
    if not isinstance(amounts_csv, str):
        return None
    amounts = [_num(a) for a in amounts_csv.split(',')]
    if not amounts or any(a is None for a in amounts):
        return None
    return min(sum(amounts), MAX_FINE_TOTAL)


def speed_excess(reading):
    """Percent over limit for 'speed/limit'. Returns None if invalid or limit == 0."""
    if not isinstance(reading, str):
        return None
    parts = reading.split('/')
    if len(parts) != 2:
        return None
    speed, limit = _num(parts[0]), _num(parts[1])
    if speed is None or limit is None or limit == 0:
        return None
    return (speed - limit) * 100 // limit


def _show(label, value):
    print(label, value if value is not None else "Invalid input")


def main():
    print("==== Running parse_ticket_id ====")
    user_input = input("Enter a ticket ID (e.g. TF-2024-0456): ")
    _show("Ticket Prefix, Year and Serial:", parse_ticket_id(user_input))

    print("\n==== Running total_fines ====")
    user_input = input("Enter fine amounts as CSV (e.g. 500,1200,300): ")
    _show("Total Fines:", total_fines(user_input))

    print("\n==== Running speed_excess ====")
    user_input = input("Enter speed/limit (e.g. 72/60): ")
    _show("Percent Over Limit:", speed_excess(user_input))


if __name__ == "__main__":
    main()
