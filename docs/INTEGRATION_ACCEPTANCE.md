# Integration acceptance matrix

Engine verification uses bundled records in the specified product. Live integration verification requires a real collector or query endpoint and recorded linked evidence.

| Surface | Verification state | Evidence or prerequisite |
| --- | --- | --- |
| Community Lite, Linux x86-64 | Integration-verified locally | Compose health, 40 lesson pages, fixture outcomes, browser reports, and reset. [Validation summary](../reports/validation-summary.md) |
| Static showcase | Integration-verified on local HTTP | Relative assets, all lesson navigation, fixture comparisons, and browser-local reports under a project subpath. [Showcase](../public-demo/README.md) |
| GitHub Pages hosting | Manual pending | Apply reviewed workflow on `main` and select GitHub Actions as the Pages source. |
| Sigma | Static-validated and synthetic-verified | 40 rules, pySigma reference resolution, and local projection selection tests. |
| Wazuh | Isolated engine verified with synthetic data | The 4.14.10 engine exercises its decoder and 20 event-level rules. A manager, indexer, dashboard, and agent deployment require separate verification. [Report](../detections/wazuh/engine-validation.json) |
| Windows Sysmon agent | Synthetic adapter verified | Sysmon XML projects to the Event schema. Await a Windows VM with configured agent and manager. |
| Linux audit agent | Synthetic adapter verified | Linux `SYSCALL` log projects to the Event schema. Await disposable VM agent collection. |
| Zeek and Suricata | Synthetic adapter verified | Native-shaped DNS projections and offline PCAP baseline. Await runs with the actual sensors. |
| YARA | Optional engine verified with synthetic data | One local training-note match and one clean control. |
| Velociraptor | Documented | Await authorized client enrollment, scoped collection and recorded result. |
| Sentinel KQL / Defender XDR | Offline mapping and template checks | Await approved licensed service and query results. |
| Splunk SPL | Offline mapping and template checks | Await approved index, sourcetype and query results. |
| AWS, Entra, GitHub Audit, Kubernetes | Synthetic adapter verified | Await authorized provider collection and join validation. See linked fields and prerequisites. |
| Windows and macOS Docker Desktop | Manual pending | Run the platform smoke checks in Docker Desktop. |

[Setup](full-lab-setup.md) · [Vendor samples](VENDOR_SAMPLES.md) · [Portability](PORTABLE_DETECTIONS.md) · [Desktop platform instructions](WINDOWS_AND_MACOS.md)
