# Evidence and technique coverage

The local engine runs three labeled batches per scenario. The local validation column covers the bundled fixture set. All 40 scenarios have an original Sigma specification with offline pySigma and fixture-selection checks. The 10 core lessons also have dedicated browser smoke tests.

[Machine-readable scenario matrix](scenario-matrix.json)

| ID | Lesson | Enterprise ATT&CK | Local fixture result | Guided coverage | Wazuh | KQL/SPL |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | [Phishing](learn/01.md) | [T1566.002](https://attack.mitre.org/techniques/T1566/002) direct | Synthetic-verified | Core | Engine verified on synthetic records | Review |
| 02 | [MFA Fatigue](learn/02.md) | [T1621](https://attack.mitre.org/techniques/T1621) direct | Synthetic-verified | Core | Engine verified on synthetic records | Review |
| 03 | [Password Spraying](learn/03.md) | [T1110.003](https://attack.mitre.org/techniques/T1110/003) direct | Synthetic-verified | Core | Engine verified on synthetic records | Review |
| 04 | [Public-Facing Application Exploits](learn/04.md) | [T1190](https://attack.mitre.org/techniques/T1190) direct | Synthetic-verified | Additional | Engine verified on synthetic records | Review |
| 05 | [OAuth Consent Phishing](learn/05.md) | [T1528](https://attack.mitre.org/techniques/T1528) related | Synthetic-verified | Additional | Engine verified on synthetic records | Review |
| 06 | [PowerShell Abuse](learn/06.md) | [T1059.001](https://attack.mitre.org/techniques/T1059/001) direct | Synthetic-verified | Core | Engine verified on synthetic records | Review |
| 07 | [HTML Smuggling](learn/07.md) | [T1027.006](https://attack.mitre.org/techniques/T1027/006) direct | Synthetic-verified | Additional | Engine verified on synthetic records | Review |
| 08 | [Scheduled Tasks/Cron](learn/08.md) | [T1053.003](https://attack.mitre.org/techniques/T1053/003) direct | Synthetic-verified | Additional | Engine verified on synthetic records | Review |
| 09 | [Registry Autoruns](learn/09.md) | [T1547.001](https://attack.mitre.org/techniques/T1547/001) direct | Synthetic-verified | Core | Engine verified on synthetic records | Review |
| 10 | [WMI Subscription](learn/10.md) | [T1546.003](https://attack.mitre.org/techniques/T1546/003) direct | Synthetic-verified | Additional | Engine verified on synthetic records | Review |
| 11 | [Token Theft](learn/11.md) | [T1550.001](https://attack.mitre.org/techniques/T1550/001) related | Synthetic-verified | Additional | Engine verified on synthetic records | Review |
| 12 | [Credential Dumping](learn/12.md) | [T1003.001](https://attack.mitre.org/techniques/T1003/001) direct | Synthetic-verified | Additional | Engine verified on synthetic records | Review |
| 13 | [Kerberoasting](learn/13.md) | [T1558.003](https://attack.mitre.org/techniques/T1558/003) direct | Synthetic-verified | Additional | Engine verified on synthetic records | Review |
| 14 | [Pass-the-Hash](learn/14.md) | [T1550.002](https://attack.mitre.org/techniques/T1550/002) related | Synthetic-verified | Additional | Engine verified on synthetic records | Review |
| 15 | [Privilege Escalation](learn/15.md) | [T1068](https://attack.mitre.org/techniques/T1068) related | Synthetic-verified | Additional | Engine verified on synthetic records | Review |
| 16 | [RDP/SMB/WinRM Abuse](learn/16.md) | [T1021](https://attack.mitre.org/techniques/T1021) direct | Synthetic-verified | Core | Engine verified on synthetic records | — |
| 17 | [LOLBins/LOLBAS](learn/17.md) | [T1218](https://attack.mitre.org/techniques/T1218) direct | Synthetic-verified | Additional | Engine verified on synthetic records | — |
| 18 | [Disable Security Tools](learn/18.md) | [T1685](https://attack.mitre.org/techniques/T1685) direct | Synthetic-verified | Additional | Engine verified on synthetic records | — |
| 19 | [HTTPS/DNS Command & Control](learn/19.md) | [T1071.004](https://attack.mitre.org/techniques/T1071/004) direct | Synthetic-verified | Additional | Engine verified on synthetic records | — |
| 20 | [Cloud IAM Abuse](learn/20.md) | [T1098.003](https://attack.mitre.org/techniques/T1098/003) direct | Synthetic-verified | Core | Engine verified on synthetic records | — |
| 21 | [Active Directory Enumeration](learn/21.md) | [T1087.002](https://attack.mitre.org/techniques/T1087/002) direct | Synthetic-verified | Additional | — | — |
| 22 | [Cloud Exfiltration](learn/22.md) | [T1530](https://attack.mitre.org/techniques/T1530) related | Synthetic-verified | Additional | — | — |
| 23 | [Ransomware-Like Activity](learn/23.md) | [T1486](https://attack.mitre.org/techniques/T1486) related | Synthetic-verified | Core | — | — |
| 24 | [Data Staging](learn/24.md) | [T1560.001](https://attack.mitre.org/techniques/T1560/001) direct | Synthetic-verified | Additional | — | — |
| 25 | [Wiper-Like Activity](learn/25.md) | [T1485](https://attack.mitre.org/techniques/T1485) direct | Synthetic-verified | Additional | — | — |
| 26 | [Adversary-in-the-Middle Phishing](learn/26.md) | [T1557](https://attack.mitre.org/techniques/T1557) related | Synthetic-verified | Additional | — | — |
| 27 | [Device-Code Phishing](learn/27.md) | [T1566.002](https://attack.mitre.org/techniques/T1566/002) related | Synthetic-verified | Additional | — | — |
| 28 | [Browser Cookie Theft](learn/28.md) | [T1539](https://attack.mitre.org/techniques/T1539) direct | Synthetic-verified | Additional | — | — |
| 29 | [Infostealers](learn/29.md) | [T1555.003](https://attack.mitre.org/techniques/T1555/003) direct | Synthetic-verified | Additional | — | — |
| 30 | [QR-Code Phishing](learn/30.md) | [T1566.002](https://attack.mitre.org/techniques/T1566/002) direct | Synthetic-verified | Additional | — | — |
| 31 | [Malicious Dependencies](learn/31.md) | [T1195.001](https://attack.mitre.org/techniques/T1195/001) direct | Synthetic-verified | Additional | — | — |
| 32 | [CI/CD Token Compromise](learn/32.md) | [T1550.001](https://attack.mitre.org/techniques/T1550/001) related | Synthetic-verified | Additional | — | — |
| 33 | [GitHub Actions Tampering](learn/33.md) | [T1677](https://attack.mitre.org/techniques/T1677) related | Synthetic-verified | Core | — | — |
| 34 | [Secrets in Git/Artifacts](learn/34.md) | [T1552.001](https://attack.mitre.org/techniques/T1552/001) related | Synthetic-verified | Additional | — | — |
| 35 | [Kubernetes RBAC Abuse](learn/35.md) | [T1098.006](https://attack.mitre.org/techniques/T1098/006) direct | Synthetic-verified | Core | — | — |
| 36 | [Container Escape](learn/36.md) | [T1611](https://attack.mitre.org/techniques/T1611) related | Synthetic-verified | Additional | — | — |
| 37 | [Cloud Metadata Credential Theft](learn/37.md) | [T1552.005](https://attack.mitre.org/techniques/T1552/005) direct | Synthetic-verified | Additional | — | — |
| 38 | [BYOVD Driver Abuse](learn/38.md) | [T1068](https://attack.mitre.org/techniques/T1068) related | Synthetic-verified | Additional | — | — |
| 39 | [RMM Tool Abuse](learn/39.md) | [T1219.002](https://attack.mitre.org/techniques/T1219/002) direct | Synthetic-verified | Additional | — | — |
| 40 | [SaaS Exfiltration](learn/40.md) | [T1567](https://attack.mitre.org/techniques/T1567) related | Synthetic-verified | Additional | — | — |

[Status definitions](TESTING_AND_VALIDATION.md) · [Portable detections](PORTABLE_DETECTIONS.md) · [Observed test results](../reports/validation-summary.md)
