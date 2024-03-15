import re
import ssl
import math
from contextlib import contextmanager
import paramiko
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim


def run_remote_command(host, port, username, password, cmds: list, ) -> tuple:
    """
    Run remote command

    :param host:
    :param port:
    :param username:
    :param password:
    :param cmds:
    :return: A tuple with 'host' as 1st element, and 2nd element for result of every command in 'cmds' as value(list)
    """

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port, username=username, password=password)

        result = []
        for cmd in cmds:
            _, stdout, stderr = client.exec_command(cmd)
            if stdout:
                result.append(stdout.read().decode().strip())
        return (host, result)
    except Exception as err:
        print(f"[run_remote_command]:{err}")
        return ()


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def _convert_power_state(text:str="") -> int:
    state_text = text.lower()

    if state_text == 'poweredon':
        return 0
    if state_text == 'poweredoff':
        return 1
    if state_text == 'suspended':
        return 2


def sort_by_dict_value(l: list) -> list:
    return sorted(l, key=lambda x: x['name'])

def extract_ip(text="") -> str:
    regex = r"(((25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?))"
    m = re.search(regex, text)
    if m:
        return m.group(0)
    else:
        # return "NO_IP_IN_NAME"
        return "0.0.0.0"

def _extract_sn(sn: str) -> str:
    """
    Extract serial number from sn string, which has the format below:
    '|----Serial Number............................................J301C86M'

    :param sn: String contains serial number
    :return: Serial number(i.e. J301C86M)
    """
    return sn.split('.')[-1]


def _extract_vm_info(vm) -> dict:
    power_state = _convert_power_state(str(vm.runtime.powerState))
    keys = ["name", "ip", "cpu_no", "memory", "storage", "notes", "power_state"]
    values = [
        vm.name,
        extract_ip(vm.name),
        vm.summary.config.numCpu,
        vm.summary.config.memorySizeMB,
        vm.summary.storage.committed,
        vm.summary.config.annotation,
        power_state,
    ]
    return dict(zip(keys, values))


def _extract_esxi_info(esxi) -> dict:
    """
    Extract ESXi info from pyvmomi esxi object
    Ref: https://developer.vmware.com/apis/196/vsphere

    :param esxi: pyvmomi esxi object
    :return:
    """
    # Sum total datastore size of ESXi
    storage = sum([ds.summary.capacity for ds in esxi.datastore])
    keys = ["name", "ip", "vendor", "model", "physical_cpu_no", "virtual_cpu_no", "cpu_clock_speed", "memory", "storage"]
    values = [
        esxi.name,
        esxi.name,
        esxi.hardware.systemInfo.vendor,
        esxi.hardware.systemInfo.model,
        esxi.hardware.cpuInfo.numCpuPackages,
        esxi.hardware.cpuInfo.numCpuThreads,
        esxi.hardware.cpuInfo.hz,
        esxi.hardware.memorySize,
        storage
    ]
    return dict(zip(keys, values))


@contextmanager
def get_vsphere_objects(vimtype, host: str, username: str, password: str):
    # For Ubuntu 20.04.2 LTS
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    # ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    ctx.verify_mode = ssl.CERT_NONE

    # Connect to vSphere and return a service instance
    service_instance = None
    try:
        service_instance = SmartConnect(host=host, port=443, user=username,
        # service_instance = SmartConnectNoSSL(host=host, port=443, user=username,
                                        pwd=password, sslContext=ctx)
        content = service_instance.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vimtype], True)
        yield [managed_object_ref for managed_object_ref in container.view]
    except Exception as err:
        print(f'oops: {err}')
    finally:
        Disconnect(service_instance)


def get_vcenter_info(host: str, username:str, password: str):
    """
    Get VMWare infrastructure info directly(slow)

    :return:
    """
    items = []
    with get_vsphere_objects(vim.HostSystem, host=host, username=username, password=password) as objects:
        for obj in sorted(objects, key=lambda x: x.name):
            esxi = _extract_esxi_info(obj)
            vms = []
            for vm in sorted(obj.vm, key=lambda x: x.name):
                vms.append(_extract_vm_info(vm))
            esxi["vms"] = vms
            items.append(esxi)
    return items


def get_vmware_infrastructure_info(idc: str) -> list:
    try:
        esxis = get_vcenter_info(idc)
        return sort_by_dict_value(esxis)
    except RuntimeError as err:
        print(f"get_vmware_infrastructure_info: {str(err)}")


def scan_vmware_physical_info(location: str):
    pass
#    esxis = crud.get_physical_machines_by_location(db, location)
#    if not esxis:
#        raise HTTPException(status_code=400, detail="No ESXi found, refresh first")

#    hosts = [esxi.ip for esxi in esxis]

#    cmds = [
#        '/bin/esxcfg-info 2>/dev/null  | grep "Serial Number" | grep -v "World Command"',
#    ]

#    outputs = run_parallel_func(hosts, run_remote_command,
#                                22, settings.we724_esxi_ssh_username, settings.we724_esxi_ssh_password, cmds)
#    for output in outputs:
#        if not output:
#            continue

#        # 'out' has the format below:
#        # ('192.168.100.70', ['|----Serial Number............................................J300EECX'])
#        ip, sn_str = output

#        pm_id = crud.get_physical_machine_id_by_ip(db, ip)
#        if sn_str:
#            sn = _extract_sn(sn_str[0])
#            crud.update_physical_machine_by_id(db, pm_id, infrastructure.PhysicalMachineUpdate(**{"sn": sn}))




if __name__ == "__main__":
    # esxi_host = "192.168.6.20"
    # esxi_hosts = [
    #     "192.168.6.20",
    #     "192.168.6.50",
    #     "192.168.6.60",
    #     "192.168.6.80",
    # ]
    # esxi_username = "root"
    # esxi_password = "Hexin@123"
    # for host in esxi_hosts:
    #     clusters = get_vcenter_info(host, esxi_username, esxi_password)
    #     for cluster in clusters:
    #         for vm in cluster["vms"]:
    #             name = vm["name"]
    #             status = "active" if vm["power_state"] == 0 else "offline"
    #             vcpus = vm["cpu_no"]
    #             memory = vm["memory"]
    #             cluster = host
    #             print(f"{name},{status},{vcpus},{memory},{host}")

    result = run_remote_command("192.168.2.99",22, "root", "teddy", ["ls /tmp"])
    print(result)




