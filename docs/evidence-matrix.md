# Evidence and technique coverage

The local engine runs three labeled batches per scenario. The local validation column covers the bundled fixture set. All 40 scenarios have an original Sigma specification with offline pySigma and fixture-selection checks. The 10 core lessons also have dedicated browser smoke tests.

| ID | Lesson | Enterprise ATT&CK | Local fixture result | Guided coverage | Wazuh | KQL/SPL |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | [Phishing](learn/01.md) | [T1566.002](https://attack.mitre.org/techniques/T1566/002) direct | Synthetic-verified | Core | Static test | Review |
| 02 | [MFA fatigue](learn/02.md) | [T1621](https://attack.mitre.org/techniques/T1621) direct | Synthetic-verified | Core | Static test | Review |
| 03 | [Password spraying](learn/03.md) | [T1110.003](https://attack.mitre.org/techniques/T1110/003) direct | Synthetic-verified | Core | Static test | Review |
| 04 | [Public app exploitation](learn/04.md) | [T1190](https://attack.mitre.org/techniques/T1190) direct | Synthetic-verified | Additional | Static test | Review |
| 05 | [OAuth consent phishing](learn/05.md) | [T1528](https://attack.mitre.org/techniques/T1528) related | Synthetic-verified | Additional | Static test | Review |
| 06 | [PowerShell abuse](learn/06.md) | [T1059.001](https://attack.mitre.org/techniques/T1059/001) direct | Synthetic-verified | Core | Static test | Review |
| 07 | [HTML smuggling](learn/07.md) | [T1027.006](https://attack.mitre.org/techniques/T1027/006) direct | Synthetic-verified | Additional | Static test | Review |
| 08 | [Scheduled tasks / cron](learn/08.md) | [T1053.003](https://attack.mitre.org/techniques/T1053/003) direct | Synthetic-verified | Additional | Static test | Review |
| 09 | [Registry autoruns](learn/09.md) | [T1547.001](https://attack.mitre.org/techniques/T1547/001) direct | Synthetic-verified | Core | Static test | Review |
| 10 | [WMI subscriptions](learn/10.md) | [T1546.003](https://attack.mitre.org/techniques/T1546/003) direct | Synthetic-verified | Additional | Static test | Review |
| 11 | [Token theft](learn/11.md) | [T1550.001](https://attack.mitre.org/techniques/T1550/001) related | Synthetic-verified | Additional | Static test | Review |
| 12 | [Credential dumping](learn/12.md) | [T1003.001](https://attack.mitre.org/techniques/T1003/001) direct | Synthetic-verified | Additional | Static test | Review |
| 13 | [Kerberoasting](learn/13.md) | [T1558.003](https://attack.mitre.org/techniques/T1558/003) direct | Synthetic-verified | Additional | Static test | Review |
| 14 | [Pass-the-hash](learn/14.md) | [T1550.002](https://attack.mitre.org/techniques/T1550/002) related | Synthetic-verified | Additional | Static test | Review |
| 15 | [Privilege escalation](learn/15.md) | [T1068](https://attack.mitre.org/techniques/T1068) related | Synthetic-verified | Additional | Static test | Review |
| 16 | [RDP / SMB / WinRM abuse](learn/16.md) | [T1021](https://attack.mitre.org/techniques/T1021) direct | Synthetic-verified | Core | Static test | — |
| 17 | [Living-off-the-land](learn/17.md) | [T1218](https://attack.mitre.org/techniques/T1218) direct | Synthetic-verified | Additional | Static test | — |
| 18 | [Security tool tampering](learn/18.md) | [T1685](https://attack.mitre.org/techniques/T1685) direct | Synthetic-verified | Additional | Static test | — |
| 19 | [HTTPS / DNS C2](learn/19.md) | [T1071.004](https://attack.mitre.org/techniques/T1071/004) direct | Synthetic-verified | Additional | Static test | — |
| 20 | [Cloud IAM abuse](learn/20.md) | [T1098.003](https://attack.mitre.org/techniques/T1098/003) direct | Synthetic-verified | Core | Static test | — |
| 21 | [AD enumeration](learn/21.md) | [T1087.002](https://attack.mitre.org/techniques/T1087/002) direct | Synthetic-verified | Additional | — | — |
| 22 | [Cloud storage theft](learn/22.md) | [T1530](https://attack.mitre.org/techniques/T1530) related | Synthetic-verified | Additional | — | — |
| 23 | [Ransomware-like activity](learn/23.md) | [T1486](https://attack.mitre.org/techniques/T1486) related | Synthetic-verified | Core | — | — |
| 24 | [Data staging](learn/24.md) | [T1560.001](https://attack.mitre.org/techniques/T1560/001) direct | Synthetic-verified | Additional | — | — |
| 25 | [Wiper-like activity](learn/25.md) | [T1485](https://attack.mitre.org/techniques/T1485) direct | Synthetic-verified | Additional | — | — |
| 26 | [AiTM phishing](learn/26.md) | [T1557](https://attack.mitre.org/techniques/T1557) related | Synthetic-verified | Additional | — | — |
| 27 | [Device-code phishing](learn/27.md) | [T1566.002](https://attack.mitre.org/techniques/T1566/002) related | Synthetic-verified | Additional | — | — |
| 28 | [Browser cookie theft](learn/28.md) | [T1539](https://attack.mitre.org/techniques/T1539) direct | Synthetic-verified | Additional | — | — |
| 29 | [Infostealers](learn/29.md) | [T1555.003](https://attack.mitre.org/techniques/T1555/003) direct | Synthetic-verified | Additional | — | — |
| 30 | [QR phishing](learn/30.md) | [T1566.002](https://attack.mitre.org/techniques/T1566/002) direct | Synthetic-verified | Additional | — | — |
| 31 | [Malicious dependencies](learn/31.md) | [T1195.001](https://attack.mitre.org/techniques/T1195/001) direct | Synthetic-verified | Additional | — | — |
| 32 | [CI/CD token theft](learn/32.md) | [T1550.001](https://attack.mitre.org/techniques/T1550/001) related | Synthetic-verified | Additional | — | — |
| 33 | [GitHub Actions tampering](learn/33.md) | [T1677](https://attack.mitre.org/techniques/T1677) related | Synthetic-verified | Core | — | — |
| 34 | [Secrets in Git/artifacts](learn/34.md) | [T1552.001](https://attack.mitre.org/techniques/T1552/001) related | Synthetic-verified | Additional | — | — |
| 35 | [Kubernetes RBAC abuse](learn/35.md) | [T1098.006](https://attack.mitre.org/techniques/T1098/006) direct | Synthetic-verified | Core | — | — |
| 36 | [Container escape](learn/36.md) | [T1611](https://attack.mitre.org/techniques/T1611) related | Synthetic-verified | Additional | — | — |
| 37 | [Cloud metadata theft](learn/37.md) | [T1552.005](https://attack.mitre.org/techniques/T1552/005) direct | Synthetic-verified | Additional | — | — |
| 38 | [BYOVD driver abuse](learn/38.md) | [T1068](https://attack.mitre.org/techniques/T1068) related | Synthetic-verified | Additional | — | — |
| 39 | [RMM tool abuse](learn/39.md) | [T1219.002](https://attack.mitre.org/techniques/T1219/002) direct | Synthetic-verified | Additional | — | — |
| 40 | [SaaS exfiltration](learn/40.md) | [T1567](https://attack.mitre.org/techniques/T1567) related | Synthetic-verified | Additional | — | — |

[Status definitions](TESTING_AND_VALIDATION.md) · [Portable detections](PORTABLE_DETECTIONS.md) · [Observed test results](../reports/validation-summary.md)
