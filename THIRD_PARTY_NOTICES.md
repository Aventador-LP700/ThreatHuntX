# Third-party notices

The repository's [MIT license](LICENSE) covers original ThreatHuntX code, synthetic fixtures, learning content and original media. The supplied CSV and technique maps informed the organization and lesson topics. The repository includes newly authored content and diagrams.

## MITRE ATT&CK®

The technique identifiers, names, tactics and reference URLs in `scenarios/attack` and the derivative lesson materials come from Enterprise ATT&CK 20.1, commit `f59b03ecf828579d5f9e93683ce25b7e2e5fd9d7`.

> © 2026 The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation.

[MITRE ATT&CK distribution license](docs/licenses/MITRE-ATTACK.txt) · [MITRE terms](https://attack.mitre.org/resources/terms-of-use/) · [Pinned source](https://github.com/mitre-attack/attack-stix-data/tree/f59b03ecf828579d5f9e93683ce25b7e2e5fd9d7/enterprise-attack)

## Frontend notices

The Vue build includes Vue and Vue Router under MIT and Lucide icons under ISC with Feather portions under MIT. Preserve the following texts when distributing the compiled application.

[Vue license](docs/licenses/Vue.txt) · [Vue Router license](docs/licenses/Vue-Router.txt) · [Lucide and Feather licenses](docs/licenses/Lucide.txt)

## Runtime, development, and referenced tools

Runtime and tooling dependencies are resolved by [uv.lock](uv.lock) and [package-lock.json](frontend/package-lock.json). Their distributions include upstream license terms. Containers are built from the pinned official Python, Node and Nginx images. See [Tools and licenses](docs/TOOLS_AND_LICENSES.md) for upstream references. The project distributes original example rules and uses Sigma specification terminology. Microsoft, Splunk, GitHub, Wazuh and other product names identify their respective tools and belong to their owners.
