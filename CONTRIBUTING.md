# Contributing

Contributions are welcome.

## Source of truth

Edit only:

```text
data/internships.csv
```

Then regenerate the public pages:

```bash
python scripts/generate_pages.py
```

Generated pages include:

- `README.md`
- `countries/united-states.md`
- `countries/china.md`
- `tracks/world-models.md`
- `tracks/multimodal.md`
- `tracks/ml-research.md`
- `tracks/robotics.md`
- `tracks/data-science.md`

## Required fields

- Company
- Role
- Country
- Location
- Track / focus area
- Degree level
- Status
- Deadline
- Application link
- Source
- Last checked date

## Status rules

- `Open`: the role or program is currently listed.
- `Watch`: a relevant employer/program worth monitoring, but a matching 2027 opening has not been verified.
- Use `Rolling` or `Not listed` when no fixed deadline is published.
- Do not guess deadlines.

## Pull requests

A good PR should:

1. Prefer an official employer link.
2. Avoid duplicate postings.
3. Update `Last Checked`.
4. Run `python scripts/generate_pages.py`.
5. Commit the regenerated Markdown pages with the CSV change.
