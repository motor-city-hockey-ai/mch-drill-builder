# Ice Hockey Systems import library

This library is reserved for diagrams and metadata imported from content Rich is authorized to access.

## Data rules

- Keep the original source diagram image. Do not redraw or generate substitute diagrams.
- Store rewritten, concise coaching instructions separately from the image.
- Preserve source title, source URL, age level, and source attribution in metadata.
- Use the normal viewer choices: **Add Diagram Only** or **Add Diagram + Instructions**.
- Do not bypass login, paywalls, access controls, or other technical restrictions. Import only content available through Rich's legitimate membership, exports, downloads, or share links and in accordance with the source site's terms.

## Expected JSON item shape

```json
{
  "uid": "ihs-0001",
  "number": 1,
  "title": "Example Drill",
  "category": "Passing / Puck Movement",
  "drill_types": ["Passing", "Small Area Games"],
  "description": "Rewritten coaching instructions.",
  "source": "Ice Hockey Systems",
  "source_url": "https://www.icehockeysystems.com/...",
  "age_level": "U12 / U14",
  "image": "data/ice-hockey-systems/images/ihs-0001.png"
}
```
