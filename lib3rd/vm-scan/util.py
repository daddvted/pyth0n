import paramiko

def run_remote_command(host, port, username, password, cmds: list, ) -> list:
    """
    Run remote command

    :param host:
    :param port:
    :param username:
    :param password:
    :param cmds:
    :return: A tuple with 'host' as 0st element, and 2nd element for result of every command in 'cmds' as value(list)
    [
        {
            "cmd": "command",
            "stdout": "hello",
            "stderr": "error,
        }
        ...
    ]
    """

    result = []
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port, username=username, password=password)

        for cmd in cmds:
            info = {
                'cmd': cmd
            }
            _, stdout, stderr = client.exec_command(cmd)
            if stdout:
                info['stdout'] = stdout.read().decode().strip()
            if stderr:
                info['stderr'] = stderr.read().decode().strip()
            result.append(info)
        return result
    except Exception as err:
        print(f"[run_remote_command]:{err}")
        return result


if __name__ == '__main__':
    cmds = [
        "virsh list --state-running --name", 
        "virsh list --all --name",
    ]
    tmp = run_remote_command("192.168.2.122", "22", "root", "hexinpas", cmds)
    print(tmp)