# SkyGuard — TODO

## Documentation
- [ ] Write the README.md (project overview, architecture, setup instructions, credentials)

## New agent tools

### Tool: seat map / amenities lookup (guest/service) — LARGER SCOPE, needs its own planning
- New table linked to aircraft_type:
  seat_number,
  position (window/aisle/middle),
  row_position (front/middle/rear of cabin),
  has_usb, has_power_outlet, has_tv
- Tool: get_seat_info(aircraft_type, seat_number) → answers questions like
  "does seat 14A have a USB port?"
- Scope warning: this requires a full seat map per aircraft type already in
  the flights table (Boeing 737, Airbus A320, etc.) — real aircraft have
  hundreds of seats each. Consider starting with ONE aircraft type as a proof
  of concept before expanding to all of them.

## Later / nice to have
- Airport code → city name mapping (e.g. "VCE" → "Venice") so agent responses
  read more naturally to passengers who don't know IATA codes