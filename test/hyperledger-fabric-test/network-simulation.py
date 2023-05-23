#!/usr/bin/python3
import re
import time
from time import localtime, strftime
import json
import subprocess
from subprocess import Popen, PIPE


def write_log(rnd, trans, msg):
    """
    :param rnd:  test round
    :param trans: traction type: query or invoke
    :param msg: message for logging
    """
    log_time = strftime("%Y%m%d %H:%M:%S", localtime())
    log = "[{}]<Round {}>({}): {}".format(log_time, rnd, trans, msg)
    print(log, flush=True)


def query_chaincode():
    cmd = 'peer chaincode query -C mychannel -n mycc -c {"Args":["query","a"]}'

    pipe = subprocess.run(cmd.split(), stdout=PIPE, stderr=PIPE)
    std_out = pipe.stdout.decode().strip()
    # print("stdout:", std_out)
    std_err = pipe.stderr.decode().strip()
    # print("stderr:", std_err)

    if std_out:
        value = re.match('.+?\s*:\s*(\d+)', std_out)
        return value.group(1)
    else:
        error = ""
        try:
            error = re.search('error.+', std_err, re.I)
            return error.group(0)
        except AttributeError as err:
            return "UNKNOWN ERR IN query_chaincode()[{}]: {}".format(err, error)


def query_till_success(rnd):
    value = query_chaincode()
    while not value.isdigit():
        # If query value is not a digit, write error to log
        write_log(rnd, "query", value)
        value = query_chaincode()
    value = int(value)
    return value


def invoke_chaincode():
    cmd = 'peer chaincode invoke -o orderer.example.com:7050 -C mychannel -n mycc -c {"Args":["invoke","a","b","1"]}'
    pipe = subprocess.run(cmd.split(), stdout=PIPE, stderr=PIPE)

    std_out = pipe.stdout.decode()
    # print("stdout:", std_out)
    std_err = pipe.stderr.decode()
    # print("stderr:", std_err)

    status = re.search('success.+status.+?(\d+)', std_err, re.I)
    if status:
        return status.group(1)
    else:
        error = ""
        try:
            error = re.search('error:.+', std_err, re.I)
            return error.group(0)
        except AttributeError as err:
            return "UNKNOWN ERR IN query_chaincode()[{}]: {}".format(err, error)


def test(rnd):
    test_info = {}
    start_time = time.time()

    # ====== Get value before invoking ======
    value_before = query_till_success(rnd)
    write_log(rnd, "query", "Query Value Before Success: {}".format(value_before))

    # ====== Invoke chaincode till success ======
    status = invoke_chaincode()
    while not status.isdigit():
        write_log(rnd, "invoke", status)
        status = invoke_chaincode()

    # ====== Get value till value changed ======
    value_after = query_till_success(rnd)
    while value_before == value_after:
        value_after = query_till_success(rnd)

    end_time = time.time()

    test_info["round"] = rnd
    test_info["startTime"] = start_time
    test_info["valueBefore"] = value_before
    test_info["valueAfter"] = value_after
    test_info["endTime"] = end_time

    return json.dumps(test_info)


if __name__ == "__main__":
    with open("data.log", "w+") as data:
        i = 0
        while True:
            line = test(i)
            print(line, file=data, flush=True)
            i += 1
