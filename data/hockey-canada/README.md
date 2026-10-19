# Canada Drill Hub library

Drills from Hockey Canada's free, publicly posted coaching PDFs (cdn.hockeycanada.ca):

- **Drill Hub sample practice plans 01–06**: 36 drills. Each one links to its Hockey Canada Drill Hub video.
- **U7 and U9 Skills Development Program practice plans 1–32**: 227 sections (warm-up, skill stations, fun game). Exact repeats across plans are merged into one entry, which lists every plan it appears in.

## Data rules

- Diagrams are the original vector diagrams, cropped from the source PDF at about 173 dpi. They are not redrawn.
- `description` and `coaching_points` are concise rewrites. The original wording stays with Hockey Canada.
- Every entry keeps `source`, `source_collection`, `source_url` (the PDF) and `source_page`. Drill Hub entries also keep `video_url`.
- For a Drill Hub station drill, the diagram is the shared three-station rink from that plan, and `station_note` says which of the three listed stations it is.
- The full Drill Hub app library needs an account and is not included. Add drills from it only through plans or exports from that account.
