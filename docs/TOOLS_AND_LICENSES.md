# Tools and licenses

The default app builds from the pinned official images in `infra/docker/`. The release health and browser checks target the assembled Linux x86-64 deployment. Each upstream image and dependency retains its own license. The application and original exercises use MIT. [Third-party notices](../THIRD_PARTY_NOTICES.md)

| Tool | Role | Upstream source or terms |
| --- | --- | --- |
| Vue and Vue Router | Local and static UI | [Vue MIT](licenses/Vue.txt) · [Router MIT](licenses/Vue-Router.txt) |
| Lucide | UI icons | [ISC and Feather MIT](licenses/Lucide.txt) |
| FastAPI, Uvicorn, Pydantic | API and data validation | [FastAPI](https://github.com/fastapi/fastapi) · [Uvicorn](https://github.com/Kludex/uvicorn) · [Pydantic](https://github.com/pydantic/pydantic) |
| SQLite | Project-local run and evidence storage | [SQLite public domain declaration](https://sqlite.org/copyright.html) |
| Nginx | Static serving and reverse proxy | [Nginx license](https://nginx.org/LICENSE) |
| MITRE ATT&CK | Technique names, tactics and references | [MITRE dataset license](licenses/MITRE-ATTACK.txt) |
| pySigma | Development-only portable specification validation | [SigmaHQ pySigma](https://github.com/SigmaHQ/pySigma) |
| Sysmon and Wazuh | Independent sensor and SIEM | [Microsoft Sysinternals](https://learn.microsoft.com/en-us/sysinternals/license-terms) · [Wazuh](https://github.com/wazuh/wazuh) |
| Zeek, Suricata, Velociraptor, kind | Optional lab tools | [Zeek](https://github.com/zeek/zeek) · [Suricata](https://github.com/OISF/suricata) · [Velociraptor](https://github.com/Velocidex/velociraptor) · [kind](https://github.com/kubernetes-sigs/kind) |

MITRE ATT&CK is a registered trademark of The MITRE Corporation. References and mappings are provided for education. Product and service names identify their respective projects. The supplied technique map was used as an input to lesson organization. Artwork and runtime media are original ThreatHuntX assets.
