#!/usr/bin/env bash

# Let's set some console colors
ERROR_MSG="[\e[91m  ERROR  \e[39m]"
WARN_MSG="[\e[93m WARNING \e[39m]"
SUCCESS_MSG="[\e[32m SUCCESS \e[39m]"
NORMAL_MSG="[\e[94m  INFO   \e[39m]"

# No action will be allowed if there is no BD created
CLIENTS=( $(for folder in `ls -d dynamic_hosts/db/prod/*`; do if [[ "${folder}" != *"test"* ]]; then basename ${folder:1}; fi; done) )
if [[ -z "$CLIENTS" ]]; then
    echo -e "$ERROR_MSG No client has yet been defined"
    echo -e "$ERROR_MSG Please first capture some servers for some client"
    echo -e "$ERROR_MSG Test clients are not valid"
    echo -e "$ERROR_MSG To add a server use one of the following commands:"
    echo -e "$ERROR_MSG   hosts.py --client <CLIENT_NAME> --new-server"
    echo -e "$ERROR_MSG   python3 hosts.py --client <CLIENT_NAME> --new-server"
    exit 1
fi

# If the first parameter is not a valid client
# then it is necessary to show an error message and determine the execution of this script
if [[ -z "$1" ]] || [[ -z "$(echo "${CLIENTS[@]:0}" | grep -ow $1)" ]]; then
    echo -e "$ERROR_MSG  You need to specify the client's name as the first parameter."
    echo -e "${NORMAL_MSG}  The available clients are:"

    for i in "${CLIENTS[@]}"
    do
        echo -e "${NORMAL_MSG}  - $i"
    done

    exit 1
fi

DEPLOY_VERSION="0.0.1"
DESCRIPTION="This script allows you to run a playbook in a container using a dynamic host list."

IMAGE_NAME=dynamic_hosts:latest
BUILD_ENV_PROJECT=$(pwd)
ENVIRONMENTS=( "all" "pro" "itg" "dev" )
ROLES=( "all" "app" "db" "web" "zoo" )
THE_GROUPS=( "all" "self" )
LOCAL_SSH="$(dirname ~/.ssh)/.ssh"
KNOWN_HOSTS_FILE=

CLIENT=$1
shift 1

DOCKER_CMD=
SRC_DIR=
CONTAINER_PROXY=

CLIENT_FILER="--env THE_CLIENT=$CLIENT"
GROUP_FILTER=""
ENV_FILTER=""
ROLE_FILTER=""
EXTRAS=

help_header()
{
    echo "|--------------------------------------------------------------------------------|"
    echo -e "|     \e[36mA N S I B L E   W I T H   D Y N A M I C   H O S T S\e[39m            |"
    echo "|--------------------------------------------------------------------------------|"
    printf "|%20s ... %-65s|\n" "Current environment" "$(echo -e "\e[97m${1}\e[39m")"
    printf "|%20s ... %-65s|\n" "Script Version" "$(echo -e "\e[97m${DEPLOY_VERSION}\e[39m")"
    printf "|%20s ... %-65s|\n" "Bash Version" "$(echo -e "\e[97m$BASH_VERSION\e[39m")"
    printf "|%20s ... %-65s|\n" "Description" "$(echo -e "\e[97m$DESCRIPTION\e[39m")"
    echo "|--------------------------------------------------------------------------------|"
}

usage()
{
    help_header
    echo ""
    echo " Usage:"
    echo -e "  \e[97m$(basename $0)\e[39m CLIENT [ENVIRONMENT] [GROUP] [ROLES]"
    echo ""
    echo " Client:"
    for i in "${CLIENTS[@]}"
    do
        echo "        $i"
    done
    echo " Environment:"
    echo "   -e|--env        It sets the environment of the hosts."
    echo "                   If omitted, all environments will be used."
    echo " The available environments are:"
    for i in "${ENVIRONMENTS[@]}"
    do
        echo "        $i"
    done
    echo " Groups:"
    echo "   -g|--group       It sets the group of the hosts."
    echo -e "                    If omitted, a group called \e[97mall\e[39m will be used."
    echo " The available groups are:"
    for i in "${THE_GROUPS[@]}"
    do
        echo "        $i"
    done
    echo " Roles:"
    echo "   -e|--env         It sets the role of the hosts."
    echo "                   If omitted, all roles will be used."
    echo " The available roles are:"
    for i in "${ROLES[@]}"
    do
        echo "        $i"
    done
    echo ""
    echo " Expamples:"
    echo -e "  \e[97m$(basename $0)\e[39m ${CLIENTS[1]}"
    echo "  It will execute the playbbok on all the hosts of the client ${CLIENTS[1]}. The hosts will be grouped into a group called all."
    printf "  {
      \"all\": {
          \"hosts\": [
              \"hosta.domain.net\",
              \"hostb.domain.net\"
          ],
          \"vars\": {}
      }
  }\n"
    echo ""
    echo -e "  \e[97m$(basename $0)\e[39m ${CLIENTS[0]} -e ${ENVIRONMENTS[1]}"
    echo "  Execute playbbok on all hosts of client ${CLIENTS[0]} that belong to environment ${ENVIRONMENTS[1]}. The hosts will be grouped into a group called all."
    printf "  {
      \"all\": {
          \"hosts\": [
              \"hostc.domain.net\",
              \"hostd.domain.net\"
          ],
          \"vars\": {}
      }
  }\n"
    echo ""
    echo -e "  \e[97m$(basename $0)\e[39m ${CLIENTS[0]} -g ${THE_GROUPS[1]}"
    echo "  It will execute the playbbok on all hosts of client ${CLIENTS[0]} and they will be grouped in the group to which they belong."
    printf "  {
      \"PRO\": {
          \"hosts\": [
              \"hosta.domain.net\",
              \"hostb.domain.net\"
          ],
          \"vars\": {}
      }
      \"DEV\": {
          \"hosts\": [
              \"hostc.domain.net\",
              \"hostd.domain.net\"
          ],
          \"vars\": {}
      }
  }\n"
}

if [[ $# -gt 0 ]]; then
    while [[ "$1" != "" ]]; do
        case $1 in
            -e|--env)
                if [[ ! -z "$(echo "${ENVIRONMENTS[@]:0}" | grep -ow $2)" ]]; then
                    ENV_FILTER="--env THE_ENVIRONMENT=$2"
                else
                    echo -e "$ERROR_MSG Unknown environment option: $2"
                    usage
                    exit 1
                fi
                shift 2
                continue
                ;;
            -g|--group)
                if [[ ! -z "$(echo "${THE_GROUPS[@]:0}" | grep -ow $2)" ]]; then
                    GROUP_FILTER="--env THE_GROUP=$2"
                else
                    echo -e "$ERROR_MSG Unknown group option: $2"
                    usage
                    exit 1
                fi
                shift 2
                continue
                ;;
            -r|--role)
                if [[ ! -z "$(echo "${ROLES[@]:0}" | grep -ow $2)" ]]; then
                    ROLE_FILTER="--env THE_ROLE=$2"
                else
                    echo -e "$ERROR_MSG Unknown role option: $2"
                    usage
                    exit 1
                fi
                shift 2
                continue
                ;;
            -h|-\?|--help|help)
                usage
                exit 0
                ;;
            --)              # End of all options.
                shift
                break
                ;;
            *)
                #echo -e "$ERROR_MSG Unknown option: $1"
                #usage
                #exit 1
                ;;
        esac
        EXTRAS="$EXTRAS $1"
        shift
    done
fi

if [[ -z "$(git --version | grep windows)" ]]; then
    DOCKER_CMD=$(which docker)
    BUILD_ENV_PROJECT=$(pwd)/automation
    SRC_DIR=/src
else
    DOCKER_CMD="winpty docker"
    BUILD_ENV_PROJECT=/$(pwd)/automation
    SRC_DIR=//src
    LOCAL_SSH=$(dirname ~/.ssh)/.ssh
fi

prepare_ssh_dir()
{
    if [[ ! -d ./ssh ]]; then
        mkdir ./ssh
    fi

    local files=( "id_rsa" "id_rsa.pub" "known_hosts" )

    for file in "${files[@]}"
    do
        local origin=${LOCAL_SSH}/${file}
        local destination=./ssh/${file}

        if [[ ! -f "$origin" ]]; then
            echo -e "$ERROR_MSG Unable to find '$origin' file"
            exit 2
        fi

        echo -e "${NORMAL_MSG} Copying $file file"
        cp ${origin} ${destination}

        if [[ "$(md5sum ${origin} | cut -d' ' -f1)" != "$(md5sum ${destination} | cut -d' ' -f1)" ]]; then
            echo -e "$ERROR_MSG Something went wrong"
            exit 2
        fi

        echo -e "$SUCCESS_MSG Successful copy"
    done
}

image_exist()
{
    local result=0
    local image_id=$(docker images -q ${IMAGE_NAME})

    if [[ "$image_id" != "" ]]; then
        result=1
    fi

    return ${result}
}

build_image()
{
    local image_id=$(docker images -q ${IMAGE_NAME})

    if [[ "$image_id" != "" ]]; then
        # The image exists, so we must first make sure that there is no container based on this image running.
        CONTAINERS=$(docker ps -af ancestor="$image_id" --format '{{.Names}}')

        for container in ${CONTAINERS}
        do
            container_is_running ${container}

            if [[ $? -eq 1 ]]; then
                echo -e "$WARN_MSG killing container ${container}"
                ${DOCKER_CMD} container kill ${container}
            fi

            echo -e "$WARN_MSG deleting container ${container}"
            ${DOCKER_CMD} container rm -f ${container}
        done

        echo -n "Do you want to delete the existing image (Y/n)? "
        read -n1 ans

        if [[ -z "$ans" ]] || [[ "$ans" == "y" ]] || [[ "$ans" == "Y" ]]; then
            ${DOCKER_CMD} rmi -f ${image_id}
        fi
    fi

    prepare_ssh_dir

    # Let's prepare the proxy configuration
    local proxy=''
    if [[ "${https_proxy}" != "" ]]; then
        proxy="--build-arg https_proxy=$https_proxy"
    fi

    if [[ "${http_proxy}" != "" ]]; then
        proxy="$proxy --build-arg http_proxy=$http_proxy"
    fi

    echo -e "${NORMAL_MSG} building '${IMAGE_NAME}' image"
    ${DOCKER_CMD} build ${proxy} -t ${IMAGE_NAME} .

    rm -fr ./ssh
}

image_exist

if [[ $? -eq 0 ]]; then
    build_image
fi

if [[ "${https_proxy}" != "" ]]; then
    CONTAINER_PROXY="--env https_proxy=$https_proxy"
fi

if [[ "${http_proxy}" != "" ]]; then
    CONTAINER_PROXY="${CONTAINER_PROXY} --env http_proxy=$http_proxy"
fi

${DOCKER_CMD} run -it --rm -w ${SRC_DIR} ${CONTAINER_PROXY} ${CLIENT_FILER} ${ENV_FILTER} ${GROUP_FILTER} ${ROLE_FILTER} -e LOCK_NAME=ansible-playbook-${USER} ${IMAGE_NAME} ansible-playbook -v playbook/playbook.yml -i hosts.py -e do_retry=false ${TAGS} ${EXTRAS}
