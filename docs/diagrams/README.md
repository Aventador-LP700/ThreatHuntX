# ThreatHuntX diagrams and images

Download the framework infographic, architecture diagrams, and screenshots in SVG, PNG, or PDF. The architecture SVGs and PDFs retain scalable text and shapes. For the infographic, screenshots, and radar illustration, SVG and PDF embed the original-resolution image.

## Diagrams

| Diagram | SVG | PNG | PDF | Editable source |
| --- | --- | --- | --- | --- |
| Community Lab architecture | [SVG](svg/architecture.svg) | [PNG](png/architecture.png) | [PDF](pdf/architecture.pdf) | [Graphviz](sources/architecture.dot) |
| Deployed network and data boundaries | [SVG](svg/lite-boundaries.svg) | [PNG](png/lite-boundaries.png) | [PDF](pdf/lite-boundaries.pdf) | [Graphviz](sources/lite-boundaries.dot) |
| Evidence and detection data flow | [SVG](svg/data-flow.svg) | [PNG](png/data-flow.png) | [PDF](pdf/data-flow.pdf) | [Mermaid](../architecture.mmd) |
| Community Lite, static showcase, and analyst lab boundaries | [SVG](svg/lab-boundaries.svg) | [PNG](png/lab-boundaries.png) | [PDF](pdf/lab-boundaries.pdf) | [Mermaid](../lite-boundaries.mmd) |
| Optional analyst topology | [SVG](svg/optional-analyst-topology.svg) | [PNG](png/optional-analyst-topology.png) | [PDF](pdf/optional-analyst-topology.pdf) | [Mermaid](sources/optional-analyst-topology.mmd) |

The optional analyst diagram labels live collection and integrations by verification state. [Architecture and integration scope](../REFERENCE_ARCHITECTURE.md)

## Scenario map and application images

| Image | SVG | PNG | PDF | WebP preview |
| --- | --- | --- | --- | --- |
| Original ThreatHuntX v2 framework infographic | [SVG](svg/threathuntx-v2-40-threat-map.svg) | [PNG](png/threathuntx-v2-40-threat-map.png) | [PDF](pdf/threathuntx-v2-40-threat-map.pdf) | [WebP](../media/threathuntx-v2-40-threat-map.webp) |
| Technique Map with all 40 scenario and countermeasure pairs | [SVG](svg/v2-technique-map.svg) | [PNG](png/v2-technique-map.png) | [PDF](pdf/v2-technique-map.pdf) | [WebP](../media/v2-technique-map.webp) |
| Community Lab home | [SVG](svg/intro.svg) | [PNG](png/intro.png) | [PDF](pdf/intro.pdf) | [WebP](../media/intro.webp) |
| Guided MFA replay | [SVG](svg/guided-replay.svg) | [PNG](png/guided-replay.png) | [PDF](pdf/guided-replay.pdf) | [WebP](../media/guided-replay.webp) |
| Alert evidence timeline | [SVG](svg/evidence-timeline.svg) | [PNG](png/evidence-timeline.png) | [PDF](pdf/evidence-timeline.pdf) | [WebP](../media/evidence-timeline.webp) |
| ATT&CK matrix | [SVG](svg/attack-matrix.svg) | [PNG](png/attack-matrix.png) | [PDF](pdf/attack-matrix.pdf) | [WebP](../media/attack-matrix.webp) |
| Detection rule view | [SVG](svg/detection-rule.svg) | [PNG](png/detection-rule.png) | [PDF](pdf/detection-rule.pdf) | [WebP](../media/detection-rule.webp) |
| Detection Studio fixture comparison | [SVG](svg/v2-detection-studio.svg) | [PNG](png/v2-detection-studio.png) | [PDF](pdf/v2-detection-studio.pdf) | [WebP](../media/v2-detection-studio.webp) |
| Printable case report | [SVG](svg/v2-case-report.svg) | [PNG](png/v2-case-report.png) | [PDF](pdf/v2-case-report.pdf) | [WebP](../media/v2-case-report.webp) |
| Workspace radar illustration | [SVG](svg/radar.svg) | [PNG](png/radar.png) | [PDF](pdf/radar.pdf) | [WebP](../../frontend/src/assets/radar.webp) |

The framework infographic measures 1536 × 1024 pixels. The Technique Map capture from the application measures 2109 × 2244 pixels. The full catalog is also available as accessible text and JSON. [40 walkthroughs](../evidence-matrix.md) · [Scenario data](../scenario-matrix.json) · [MFA replay recording](../media/mfa-replay.mp4)

## Export sources

- Render the Graphviz sources with `dot -Tsvg`. The existing PNGs use `dot -Gdpi=128 -Tpng` with DejaVu Sans.
- Render the `.mmd` files with Mermaid 11.12.0 using the neutral theme and SVG text labels. Apply styles as SVG presentation attributes before exporting to PNG and one-page PDF with Inkscape.
- Convert a WebP to PNG at its original dimensions. Embed that PNG in an SVG `<image>` with a matching `viewBox`. ReportLab can place the PNG on a single PDF page with lossless compression and alpha support.
