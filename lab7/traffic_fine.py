def parse_ticket_id(ticket_id):
    prefix, year, serial = ticket_id.split('-')
    return prefix.upper(), int(year), int(serial)

def total_fines(amounts_csv):
    amounts = [int(a) for a in amounts_csv.split(',')]
    return min(sum(amounts), 10000)

def speed_excess(reading):
    speed, limit = reading.split('/')
    return (int(speed) - int(limit)) * 100 // int(limit)
