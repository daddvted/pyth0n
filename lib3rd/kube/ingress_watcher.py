import subprocess
from kubernetes import client, config, watch
config.load_kube_config()

BIND9_FILE_MAP = {
    "shit.local": "db.shit.local",
    "dev.shit.local": "db.dev.shit.local",
    "devops.shit.local": "db.devops.shit.local",
}
INGRESS_ADDR = "192.168.2.53"


def extract_host_domain(text: str) -> tuple:
    return tuple(text.split(".", 1))


v1_api = client.CoreV1Api()
networking_api = client.NetworkingV1beta1Api()

watcher = watch.Watch()

for event in watcher.stream(networking_api.list_ingress_for_all_namespaces):
    event_type = event["type"].lower()
    event_obj_spec = event["object"].spec

    if event_type in ["added", "deleted"]:
        for rule in event_obj_spec.rules:
            if rule.host.endswith("shit.local"):
                host, domain = extract_host_domain(rule.host)
                zone_file = BIND9_FILE_MAP[domain]

                if event_type == "added":
                    print(f"bash dns-entry-tool.sh -t add -f {zone_file} -n {host} -i {INGRESS_ADDR}")
                else:
                    print(f"bash dns-entry-tool.sh -t del -f {zone_file} -n {host}")


