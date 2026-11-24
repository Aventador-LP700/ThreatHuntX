# Optional analyst lab

The Community Lab is self-contained. The components below are independent, opt-in setups for disposable machines. Live collection and end-to-end provider integrations are **manual pending** for the alpha. The versions and release links were checked against their publishers. Use current patched builds of the listed compatibility lines if a security update supersedes a pin, and record the exact versions you use.

## Wazuh 4.14.10

Use Wazuh manager, indexer and dashboard from the same [v4.14.10 Docker release](https://github.com/wazuh/wazuh-docker/tree/76ddb88b9c8b618a254a287f2684f93d3c5ac2f4/single-node). Follow the [official single-node and certificate instructions](https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html) on a dedicated VM. Wazuh's Docker guide lists 4 CPU cores, 8 GB RAM and 50 GB of disk as prerequisites. The full lab uses more resources than the two-service Community Lab. Use the upstream host configuration instructions for OpenSearch limits. Keep and restore any previous host settings when tearing down your lab VM.

Before starting, replace upstream demonstration passwords and generate dedicated certificates following the Wazuh credential setup. Keep the files outside Git. Remove host publication of indexer `9200/TCP` and API `55000/TCP` unless needed for administration. Bind dashboard HTTPS to loopback and tunnel it through approved access. On a dedicated agent network, allow `1514/TCP` for agent events and `1515/TCP` for enrollment only from assigned lab agents. Keep bulk collectors and any syslog listener private. Protect the API, indexer and dashboard with separate roles and firewalls.

Check `docker compose ps`, the manager logs and successful dashboard login. Back up manager rules, certificates and local index data before changes. Stop the optional project with `docker compose down` from its own working directory. Revert config or volume changes using that VM's snapshots and backups.

### Custom decoder and candidate rules

On the disposable manager, place the provided [decoder](../detections/wazuh/decoders.xml) and [candidate rules](../detections/wazuh/rules.xml) under the configured custom decoder and rule directories in `/var/ossec/etc/`. Check that IDs `100100`–`100120` are unused first. Use [wazuh-logtest](https://documentation.wazuh.com/current/user-manual/ruleset/testing.html) to submit a line from [synthetic.log](../detections/wazuh/synthetic.log). Check the decoder is `threathuntx_json` and compare the candidate rule ID with the [portable rule matrix](PORTABLE_DETECTIONS.md). For MFA the base candidate is `100102` for a denied push other than approved enrollment. A candidate may appear in a noisy batch that lacks enough distinct challenges for a local alert. Remove the two custom files and restore the previous manager configuration to roll back.

## Windows Sysmon 15.22 and Wazuh agent

Use a disposable Windows VM with an [actual Sysmon installation](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon). Pair a Wazuh agent on the [4.14 line](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-windows.html) with the manager. Use one VM snapshot before each setup. Select Sysmon event IDs 1, 6, 10, 13 and 19–21 in a reviewed Sysmon configuration. Add the `Microsoft-Windows-Sysmon/Operational` channel to the agent as `eventchannel`. Collect the PowerShell Operational and Security channels for lessons using 4104, 4624 and 4769. Enable the relevant audit policies centrally before attempting collection.

Confirm events in Event Viewer, check the agent reports active, and confirm the same event IDs arrive in the manager. Remove the custom channel entries, or uninstall using the publisher's steps and revert the VM snapshot when finished. Keep the agent on the dedicated network and protect its enrollment secrets.

## Linux audit, Zeek and Suricata

Install the supported Linux distribution's `auditd` package and the compatible [Linux Wazuh agent](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-linux.html) on a separate VM. Record the package version. Observe approved audit paths and send `/var/log/audit/audit.log` through the agent using the documented audit format. Verify the operator, timestamps and delivery by reviewing a known administrative log event. Roll back by removing the custom collection stanza and reverting the corresponding audit rule in the disposable VM.

For a passive network exercise, see [Zeek 9.0.1](https://github.com/zeek/zeek/releases/tag/v9.0.1) and [Suricata 8.0.8](https://github.com/OISF/suricata/tree/suricata-8.0.8). Install from the reviewed vendor packages or source release in a dedicated VM. Use only a capture you own and have approved for the exercise, or the [bundled DNS projection](../scenarios/fixtures/19.positive.json). Collect Zeek JSON `dns.log` and `conn.log` or Suricata `eve.json`, verify that the expected protocol and timestamps appear, and normalize each sensor’s fields deliberately. Stop the sensors and remove their VM when finished. A production mirror interface is outside the learning lab scope.

## Velociraptor, cloud and Kubernetes

Use an independent [Velociraptor 0.77.4](https://github.com/Velocidex/velociraptor/releases/tag/v0.77.4) server and disposable client for read-only artifact acquisition in an authorized lab. Follow its [deployment guide](https://docs.velociraptor.app/docs/deployment/). Protect administrator and enrollment credentials, verify endpoint enrollment and restrict the GUI to the administrative network. Remove the disposable client and server using vendor instructions after review.

Start cloud and Kubernetes work with packaged projections for [IAM](../scenarios/fixtures/20.positive.json), [Entra-style sign-in](../scenarios/fixtures/02.positive.json), [GitHub audit review](../scenarios/fixtures/33.positive.json) and [cluster RBAC](../scenarios/fixtures/35.positive.json). Map provider-native fields and verify timestamp, subject, approval and data boundaries before enabling a live collector. For Kubernetes practice, use a separate [kind v0.33.0](https://github.com/kubernetes-sigs/kind/releases/tag/v0.33.0) cluster with [a minimal audit policy](../infra/kind/README.md). Keep the API private and delete only the named disposable cluster at teardown.

[Validation status](../reports/validation-summary.md) · [Scope](SAFETY_AND_SCOPE.md) · [Upstream licenses and documentation](TOOLS_AND_LICENSES.md)
