# Release Log

Release version: 0.2.0-demo
Release date: 2026-04-02
Prepared by: JangKeun Kim
Approved by: Draft public release

## Summary

- Expands the public-safe benchmark from the small `v0.1` starter set to a balanced `v0.2` development and evaluation package
- Adds taxonomy, annotation, reproducibility, four audited demo release slices across `public_dev` and `public_eval`, and result-packaging layers so the release is easier to interpret and easier to extend
- Keeps the project strictly non-operational and public-facing; restricted benchmark content remains withheld

## Added

- New public items: 24 public-safe `v0.2` items across `public_dev` and `public_eval`
- New restricted items: none in the public package
- New documentation: taxonomy handbook, annotation handbook, updated benchmark card draft, and this `v0.2` release log
- New metrics or scripts: taxonomy coverage report, two public-dev and two public-eval reviewed-response comparison slices, run/release manifest generation, benchmark inventory export, markdown/CSV release scorecards, explicit slice-comparison tables, 5 visualization charts (pre/post quality, error tag reduction, mitigation delta, longitudinal quality, model heatmap), inter-rater agreement computation script, and adjudication framework with schema and handbook

## Changed

- Schema updates: run-manifest and release-manifest schemas added; scaffold validation now checks metadata artifacts
- Taxonomy changes: public-safe benchmark labels are now documented explicitly and aligned to the expanded item set
- Scoring changes: `v0.2` adds structural scorecards for release interpretation, explicit longitudinal comparison tables, and four reviewed-response comparison slices spanning `public_dev` and `public_eval`
- Governance changes: release materials now distinguish benchmark breadth, release hygiene, and audited model-response results more clearly

## Removed

- Deprecated items: none
- Retired documentation: none

## Release-class decisions

- Class A decisions: public-safe benchmark items, taxonomy docs, annotation docs, scorecards, manifests, and coverage artifacts released
- Class B decisions: release emphasizes methodology and structure rather than restricted empirical evaluation
- Class C decisions: restricted scenarios, withheld test items, and sensitive adjudication remain absent from the public package
- Class D decisions: none recorded in public materials

## Contamination notes

- New contamination risks identified: low for the current synthetic public-safe item set
- Items refreshed or replaced: `v0.2` introduces a new 24-item public benchmark layer instead of extending the `v0.1` sample set in place
- Known public exposure concerns: public evaluation items are still synthetic and should be refreshed in later releases if they become overly familiar

## Validation checks

- Schema validation: scaffold validator passes for public items, reviewed responses, run manifests, and the release manifest
- Review completion: complete reviewed-response coverage is now demonstrated for the `v0.1` demo set, two audited `v0.2` public-dev slices, and two audited `v0.2` public-eval slices, each covering two demo models
- Safety sign-off: public materials remain non-operational and do not include restricted content
- Release notes reviewed: yes
