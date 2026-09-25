# Coaches Site Drills import area

This folder is the private Motor City Hockey import target for drills that Rich has legitimately downloaded or otherwise supplied from his Coaches Site membership.

## Categories

- Station Drills
- Skill Development
- Skating
- Puckhandling
- Shooting
- Passing
- Small Area Games
- Offensive
- Defensive
- Systems
- Goalies
- Practice Plans
- Other

## Drill record schema

```json
{
  "uid": "coaches-0001",
  "number": 1,
  "title": "Drill title",
  "author": "Coach / author",
  "category": "Passing",
  "age_level": "10U-14U",
  "description": "Notes supplied or transformed from the user's files",
  "source": "The Coaches Site",
  "source_url": "https://...",
  "source_page": 1,
  "image": "data/coaches-site/images/coaches-0001.png"
}
```

The app reads `coaches-site-drills.json`. Diagrams should be individual cropped images, one drill per image, matching the existing Motor City Hockey drill-builder workflow.
