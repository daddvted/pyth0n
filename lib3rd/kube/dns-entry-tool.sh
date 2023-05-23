#!/usr/bin/env bash

FLAG=0

function usage {
  cat <<EOF
Usage: $(basename "$0") [OPTION]...
  -t    Action type: <add|del>
  -f    Bind9 DNS zone file
  -n    A record(without domain suffix)
  -i    IP address of A record specified in "-n"
  -h    display help

EOF
  exit 2
}

function log {
    msg=$1
    /bin/date +"[%Y/%m/%d %H:%M:%S]: $msg" >> $LOG
}

function add_A_record {
    # $1: zone file
    # $2: hostname
    # $3: IP address

    if [ -e "$1" ];then
        a_record_tpl="$2\t\tIN\tA\t$3"

        grep -E "$2\t" $1 &> /dev/null
        if [ "$?" -eq 0 ];then
            echo "Record $2 already exists"
        else
            echo -e "$a_record_tpl" >> $1
        fi
    else
        echo "Zone fle $1 not found !"
    fi
}

function del_A_record {
    # $1: zone file
    # $2: hostname

    if [ -e "$1" ];then
        sed -i "/$2\t/d" $1
    else
        echo "Zone fle $1 not found !"
    fi
}


# Parse command line arguments
while getopts ":t:f:n:i:h" opt; do
    case "$opt" in
        t)
            TYPE=${OPTARG}
            ([ "$TYPE" == "add" ] || [ "$TYPE" == "del" ]) || usage
            ;;
        f)
            ZONE_FILE=$OPTARG
            ;;
        n)
            HOSTNAME=$OPTARG
            ;;
        i)
            A_RECORD=$OPTARG
            ;;
        h|*)
            usage
            ;;
    esac
done
#shift $((OPTIND-1))

if [ "$TYPE" == "add" ];then
    if [ -z "${ZONE_FILE}" ] || [ -z "${HOSTNAME}" ] || [ -z "${A_RECORD}" ];then
        usage
    fi
elif [ "$TYPE" == "del" ];then
    if [ -z "${ZONE_FILE}" ] || [ -z "${HOSTNAME}" ]; then
        usage
    fi
else
    usage
fi

# Avoid globbing
set -f
BIND9_CONF_PATH=/etc/bind
PWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
LOG="$PWD/dns.log"
HOST=$(hostname)



if [ "$TYPE" == "add" ];then
    add_A_record $ZONE_FILE $HOSTNAME $A_RECORD
elif [ "$TYPE" == "del" ];then
    del_A_record $ZONE_FILE $HOSTNAME
else
    usage
fi



