from XenAPI import Session


try:
    session = Session('http://192.168.2.83/')
    session.login_with_password('root', 'hexinpass', '1.0', 'xen-api-scripts-xenapi.py')
    all = session.xenapi.VM.get_all()
    vms = []
    hosts = []
    for vm in all:
        record = session.xenapi.VM.get_record(vm)
        if not(record["is_a_template"]) and not(record["is_control_domain"]):
            print(record['name_label'], record['power_state'])
except Exception as err:
    print(err)

finally:
    session.xenapi.session.logout()
