# SANKALP Seed Dataset

This directory contains synthetic demonstration data used for local
development, testing, and demonstrations.

The data is NOT official government data and must not be presented as
real-world statistics.

## Files

- `regions.json`
- `demographics.json`
- `infrastructure.json`
- `government_projects.json`

## Relationships

All datasets use `region_id` to associate records with a region.

```text
regions
   |
   +-- demographics
   |
   +-- infrastructure
   |
   +-- government_projects