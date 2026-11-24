#!/usr/bin/env bash
# Test the pinned Wazuh analysis engine with local data in a disposable, network-disabled container.
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
if [[ $# -ne 1 || ! -r "$1" || $(uname -m) != x86_64 ]]; then
  printf 'Usage on Linux x86-64: %s /absolute/path/to/wazuh-manager_4.14.10-1_amd64.deb\n' "$0" >&2
  exit 2
fi
package=$1
image=${THX_WAZUH_TEST_IMAGE:-threathuntx-api:latest}
printf '%s  %s\n' 306babec56d241cb5b77bbc97d1aa4546d267e0a00ad8f89c773dacd70ef5686 "$package" | sha256sum -c >&2
docker image inspect "$image" > /dev/null
scratch=$(mktemp -d)
container=''
cleanup() {
  if [[ -n "$container" ]]; then docker rm -f "$container" >/dev/null; fi
  rm -rf -- "$scratch"
}
trap cleanup EXIT

dpkg-deb --fsys-tarfile "$package" | tar -x -C "$scratch" \
  ./var/ossec/bin/wazuh-analysisd ./var/ossec/bin/wazuh-logtest-legacy \
  ./var/ossec/lib/libwazuhext.so ./var/ossec/etc/internal_options.conf \
  ./var/ossec/ruleset/decoders ./var/ossec/ruleset/rules/0010-rules_config.xml
engine="$scratch/var/ossec"
mkdir -p "$engine"/{etc/rules,etc/decoders,etc/shared,queue/sockets,queue/alerts,queue/db,queue/fts,logs,var/run}
cp detections/wazuh/decoders.xml "$engine/etc/decoders/threathuntx.xml"
cp detections/wazuh/rules.xml "$engine/etc/rules/threathuntx.xml"
touch "$engine/etc/shared/ar.conf"
cat > "$engine/etc/ossec.conf" <<'CONFIG'
<ossec_config>
  <global><jsonout_output>yes</jsonout_output><alerts_log>yes</alerts_log><email_notification>no</email_notification></global>
  <ruleset>
    <decoder_dir>ruleset/decoders</decoder_dir>
    <rule_include>ruleset/rules/0010-rules_config.xml</rule_include>
    <decoder_dir>etc/decoders</decoder_dir><rule_dir>etc/rules</rule_dir>
  </ruleset>
  <rule_test><enabled>yes</enabled></rule_test>
</ossec_config>
CONFIG
sed -i 's/^analysisd.rlimit_nofile=.*/analysisd.rlimit_nofile=4096/' "$engine/etc/internal_options.conf"
container=$(docker create --network none --user 0 --cap-drop NET_RAW --entrypoint /bin/sh "$image" -c 'sleep 300')
docker cp "$engine" "$container:/var/"
docker start "$container" > /dev/null
docker exec "$container" sh -e -c '
  groupadd wazuh
  useradd -r -g wazuh -d /var/ossec -s /usr/sbin/nologin wazuh
  chmod -R a+rX /var/ossec
  chown -R wazuh:wazuh /var/ossec/queue /var/ossec/logs /var/ossec/var/run
  /var/ossec/bin/wazuh-analysisd -V
  /var/ossec/bin/wazuh-analysisd -t
' >&2
docker exec -i "$container" /var/ossec/bin/wazuh-logtest-legacy < detections/wazuh/synthetic.log 2>&1 \
  | PYTHONPATH=backend uv run --locked python -m scripts.verify_wazuh_output
