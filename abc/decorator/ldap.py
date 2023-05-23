import functools
from typing import List, Dict

from ldap3 import Server, Connection
from ldap3 import ALL, ALL_ATTRIBUTES, AUTO_BIND_NONE, SIMPLE, SUBTREE, LEVEL
from ldap3 import MODIFY_REPLACE
from ldap3.core.exceptions import *

from ld4pman.core import config
from ld4pman.core.util import logger, attribute_filter

LDAP_CONNECTION: Connection
LOG = logger()

ERROR_DICT = {
    'LDAPSocketOpenError': ['Error connecting LDAP', '6504'],
    'LDAPNoSuchObjectResult': ['Not found', '6404'],
    'LDAPInvalidCredentialsResult': ["Invalid credential", '6401'],
    'LDAPObjectClassError': ['ObjectClass error', '6500'],
    'LDAPInvalidFilterError': ['Invalid filter', '6501'],
    'LDAPEntryAlreadyExistsResult': ['Entry already exists', '6505'],
    'LDAPNotAllowedOnNotLeafResult': ['Sub entries exist', '6506'],
    'LDAPInvalidDNSyntaxResult': ['Invalid DN', '6405']
}


# Decorator to connect LDAP server
# By Ted
def connect2ldap(host='localhost', port=389, username='', password='', do_binding=True):
    def wrapper_opt(func):
        @functools.wraps(func)  # Keep decorated function's real name
        def wrapper(*args, **kwargs):  # Pass arguments to decorated func
            try:
                server = Server(host=host, port=port, connect_timeout=5, use_ssl=config.LDAP_SSL_ENABLED, get_info=ALL)
                global LDAP_CONNECTION

                # Use username and password in wrapped function
                if "username" in kwargs and 'password' in kwargs:
                    actual_user = kwargs['username']
                    actual_pass = kwargs['password']
                # Use username and password in decorator
                else:
                    actual_user = username
                    actual_pass = password

                # print(f'Actual user: {actual_user}, Actual pass: {actual_pass}')
                LOG.info(f'Actual user: {actual_user}, Actual pass: ******')

                if actual_user and actual_pass:
                    LDAP_CONNECTION = Connection(server, user=actual_user, password=actual_pass,
                                                 auto_bind=AUTO_BIND_NONE,
                                                 raise_exceptions=True)
                else:  # Anonymous bind
                    LOG.info('Use Anonymous bind')
                    LDAP_CONNECTION = Connection(server, raise_exceptions=True)
                if do_binding:
                    LDAP_CONNECTION.bind()
                return func(*args, **kwargs)
            except (LDAPSocketOpenError, LDAPInvalidCredentialsResult, LDAPNoSuchObjectResult,
                    LDAPObjectClassError, LDAPObjectClassViolationResult, LDAPInvalidFilterError,
                    LDAPNotAllowedOnNotLeafResult, LDAPEntryAlreadyExistsResult, LDAPInvalidDNSyntaxResult) as err:
                # print('{}: {}'.format(type(err).__name__, err))
                LOG.error(f'{err}')
                exception_name = type(err).__name__
                labels = ['msg', 'code']
                values = ERROR_DICT.get(exception_name, ['unknown error', '6000'])
                exception_msg = dict(zip(labels, values))
                return exception_msg

        return wrapper

    return wrapper_opt


@connect2ldap(host=config.LDAP_HOST, port=int(config.LDAP_HOST_PORT),
              username=config.LDAP_BIND_USERNAME, password=config.LDAP_BIND_PASSWORD)
def paged_search(search_base: str, search_filter: str, search_scope: str, search_attrs: List[str]):
    if search_attrs:
        attributes = search_attrs
    else:
        attributes = ALL_ATTRIBUTES
    entries = LDAP_CONNECTION.extend.standard.paged_search(search_base=search_base,
                                                           search_filter=search_filter,
                                                           search_scope=search_scope,
                                                           attributes=attributes, paged_size=5)
    return entries  # "entries" IS A GENERATOR
    # Paged search will return raw_attributes and normal attributes:
    # [{
    #   "raw_dn": "xxx",
    #   "dn": "xxx",
    #   "raw_attributes": "xxx",
    #   "attributes": "xxx"
    #   "
    # },...]


@connect2ldap(host=config.LDAP_HOST, port=int(config.LDAP_HOST_PORT),
              username=config.LDAP_BIND_USERNAME, password=config.LDAP_BIND_PASSWORD)
def create_ldap_entry(dn: str, attrs: Dict):
    result = LDAP_CONNECTION.add(dn, attributes=attrs)
    if result:
        return {'msg': "Create successfully"}
    else:
        return {'msg': "Create failed"}


def read_ldap_entry(ldap_base: str, ldap_filter: str, ldap_scope: str, ldap_attrs: List[str]):
    entry_gen = paged_search(ldap_base, ldap_filter, ldap_scope, ldap_attrs)
    entries = list(entry_gen)
    if entries:
        entry = entries[0]
        user = {k: attribute_filter(v) for k, v in entry['attributes'].items()}
        if 'dn' not in user:
            user['dn'] = entry['dn']
        return user
    else:
        return {'msg': "Entry not found"}


@connect2ldap(host=config.LDAP_HOST, port=int(config.LDAP_HOST_PORT),
              username=config.LDAP_BIND_USERNAME, password=config.LDAP_BIND_PASSWORD)
def update_ldap_entry(gid, attrs):
    changes = {}
    # Populate changes
    for k, v in dict(attrs).items():
        changes[k] = [(MODIFY_REPLACE, [v])]
    dn = config.LDAP_GROUP_DN_TPL.format(gid, config.LDAP_GROUP_BASE)
    result = LDAP_CONNECTION.modify(dn, changes)
    if result:
        return {'msg': 'Attributes updated'}
    else:
        return {'msg': 'Update error'}


@connect2ldap(host=config.LDAP_HOST, port=int(config.LDAP_HOST_PORT),
              username=config.LDAP_BIND_USERNAME, password=config.LDAP_BIND_PASSWORD)
def delete_ldap_entry(dn: str):
    result = LDAP_CONNECTION.delete(dn)
    if result:
        return {'msg': f'{dn} deleted'}
    else:
        return {'msg': 'Delete failed'}


def list_ldap_entries(ldap_base: str, ldap_filter: str, ldap_scope: str, ldap_attrs: List[str]):
    entry_gen = paged_search(ldap_base, ldap_filter, ldap_scope, ldap_attrs)
    items = []
    # entries = list(entry_gen)

    for entry in entry_gen:
        # entry['attributes'] is a Dict
        item = {k: attribute_filter(v) for k, v in entry['attributes'].items()}
        item['dn'] = entry['dn']
        items.append(item)
    return items


def change_ldap_password(uid, old_pass, new_pass):
    try:
        user_dn = config.LDAP_USER_DN_TPL.format(uid, config.LDAP_USER_BASE)
        server = Server(host=config.LDAP_HOST, port=config.LDAP_HOST_PORT, connect_timeout=5,
                        use_ssl=config.LDAP_SSL_ENABLED, get_info=ALL)
        # Make sure Connection to raised exceptions
        with Connection(server, user=user_dn, password=old_pass, authentication=SIMPLE, raise_exceptions=True) as conn:
            conn.bind()
            conn.extend.standard.modify_password(user_dn, old_pass, new_pass)
            return {'msg': 'Password updated'}

    except (LDAPBindError, LDAPInvalidCredentialsResult, LDAPUserNameIsMandatoryError) as e:
        LOG.error('{}: {!s}'.format(e.__class__.__name__, e))
        return {'msg': '用户名或密码错误'}

    except LDAPNoSuchObjectResult as e:
        LOG.error('{}: {!s}'.format(e.__class__.__name__, e))
        return {'msg': "User not found"}

    except (LDAPSocketOpenError, LDAPExceptionError) as e:
        LOG.error('{}: {!s}'.format(e.__class__.__name__, e))
        return {'msg': '连接LDAP服务器错误'}


def max_uid_num() -> int:
    entries = list_ldap_entries(config.LDAP_USER_BASE, config.LDAP_ALL_USERS_FILTER, SUBTREE, ['uidNumber'])
    uid_numbers = []
    for entry in entries:
        # For entry that's not posixAccount(objectClass)
        if entry['uidNumber']:
            uid_numbers.append(entry['uidNumber'])
        else:
            uid_numbers.append(0)
    return max(uid_numbers)


@connect2ldap(host=config.LDAP_HOST, port=int(config.LDAP_HOST_PORT), do_binding=False)
def authenticate_user(*, username: str, password: str):
    # username must be a DN in LDAP
    return LDAP_CONNECTION.bind()
    # When bind error result will be a Dict with error message


def is_user_existent(username: str) -> bool:
    entries = paged_search(config.LDAP_USER_BASE, config.LDAP_USER_SEARCH_FILTER.format(username),
                           SUBTREE, config.LDAP_USER_ATTRS)

    return True if len(list(entries)) else False


def is_user_active(username: str) -> bool:
    entry = read_ldap_entry(config.LDAP_USER_BASE, config.LDAP_USER_SEARCH_FILTER.format(username),
                            LEVEL, ['uid', 'accountStatus'])
    return True if entry.get('accountStatus') == 'active' else False


def is_user_admin(username: str) -> bool:
    entry = read_ldap_entry(config.LDAP_USER_BASE, config.LDAP_USER_SEARCH_FILTER.format(username),
                            LEVEL, ['uid', 'domainGlobalAdmin'])
    return True if entry.get('domainGlobalAdmin') == 'yes' else False
