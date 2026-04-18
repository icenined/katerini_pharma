# katerini_pharma

A script to scrape drug dispensation records from pharmacy sites in the Katerini region (Greece) via the ECSS patient management system. This was part of an authorized effort during the 2016 Syrian Refugee Crisis in assistance of a local NGO.

## Usage

```bash
python stats.py [-o OUTFILE] [-s SITE_ID [SITE_ID ...]]
```

**Arguments:**
- `-o`, `--outfile` — output CSV filename (default: `social_pharma_<date>.csv`)
- `-s`, `--site_ids` — one or more site IDs to query (default: all sites)

**Examples:**

```bash
# Fetch all sites and save to default filename
python stats.py

# Fetch specific sites
python stats.py -s 4531 5551

# Specify output file
python stats.py -o output.csv
```

## Dependencies

```
requests
pandas
python-dateutil
beautifulsoup4
```

## Known Sites

| Site ID | Name |
|---------|------|
| 4531 | State Hospital Katerini |
| 4623 | Paionia |
| 5514 | Orefeas Skotinas |
| 5519 | Transformation |
| 5532 | N. Chranis |
| 5543 | Nireas |
| 5547 | Stone |
| 5551 | Hercules |
