# SkyGuard — TODO

## Documentation
- [ ] Write the README.md (project overview, architecture, setup instructions, credentials)

## Dataset
- [ ] Expand the training dataset
- [ ] Check for near-duplicate phrases before adding to the dataset
- [ ] Re-run the training notebook once the dataset is expanded
- [ ] Investigate the 100% test accuracy from the first training run — check for
      possible data leakage (train/test phrases too similar) before trusting it
      as a final result

## New agent tools

### Tool: calculate_fuel_load (admin only)
- Formula: (distance_km * 0.5) + (passengers * 20) = liters of fuel
- Example: 1000 km, 50 passengers → 500 + 1000 = 1500 liters
- Access: MAINTENANCE category, admin role only (same permission logic as
  existing MAINTENANCE messages)
- Needs: distance between origin/destination airports, and number
  of passengers

### Tool: lost baggage reporting (guest/service)
- New table in the database to actually store reports,
  not just have the agent respond conversationally without saving anything
- Tool: report_lost_baggage(flight_number, description) → saves the report,
  returns a reference number (e.g. "BAG-2026-0042")
- Access: SERVICE category, available to guest role

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