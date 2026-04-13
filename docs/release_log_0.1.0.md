# Release Log

Release version: 0.1.0
Release date: 2026-04-01
Prepared by: JangKeun Kim
Approved by: Draft public release

## Summary

- Initial public scaffold for CBRN-AI 2.0
- Introduces schemas, safe sample items, reviewed sample responses, templates, and a first public audit script
- Restricted benchmark content remains intentionally absent from the public release

## Added

- New public items: 6 safe sample benchmark items
- New restricted items: none
- New documentation: benchmark card draft, governance materials, release template
- New metrics or scripts: public response audit script with per-model calibration and mitigation summary output, plus scaffold validation script

## Changed

- Schema updates: first schema release for public items, restricted items, and reviewed responses
- Taxonomy changes: initial domain-family and reasoning-type labels added
- Scoring changes: first reviewed-response score families added
- Governance changes: public/restricted separation documented and enforced in scaffold layout

## Removed

- Deprecated items: none
- Retired documentation: none

## Release-class decisions

- Class A decisions: safe sample items, schemas, templates, and public audit outputs released
- Class B decisions: restricted item structure documented but not populated
- Class C decisions: no restricted internal items included in this release
- Class D decisions: none recorded in public materials

## Contamination notes

- New contamination risks identified: low for current synthetic public sample set
- Items refreshed or replaced: not applicable for initial release
- Known public exposure concerns: public sample items are synthetic and intentionally high-level

## Validation checks

- Schema validation: schema-backed scaffold validation added and public files pass validation
- Review completion: reviewed sample responses included for demo audit
- Safety sign-off: public materials remain non-operational
- Release notes reviewed: yes

## Follow-up actions

- Immediate fixes: strengthen docs around annotation workflow and expand the safe public evaluation split
- Next release priorities: starter taxonomy docs, release automation, and a larger safe public evaluation split
