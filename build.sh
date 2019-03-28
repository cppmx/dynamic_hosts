#!/usr/bin/env bash

# Let's set some console colors
ERROR_MSG="[\e[91m  ERROR  \e[39m]"
WARN_MSG="[\e[93m WARNING \e[39m]"
SUCCESS_MSG="[\e[32m SUCCESS \e[39m]"
NORMAL_MSG="[\e[94m  INFO   \e[39m]"

VERSION=$(cat version)
BUILD_DIR=$(realpath $(dirname "$0")/versions/)
DIST_FILE=dyn_hosts.${VERSION}.tar.gz
MD5_FILE=dyn_hosts.${VERSION}.md5
CONTENT_FILE=./build.txt
FORCE=0

TAR_CMD=$(which tar)
MD5_CMD=$(which md5sum)

if [[ -z "$TAR_CMD" ]]; then
    echo -e "$ERROR_MSG It is required to have the tar package installed"
    exit 1
fi

if [[ -z "$MD5_CMD" ]]; then
    echo -e "$ERROR_MSG It is required to have the md5sum package installed"
    exit 1
fi

if [[ ! -z "$1" ]]; then
    if [[ "$1" == "-f" ]]; then
        FORCE=1
    else
        echo -e "$ERROR_MSG Unknown parameter"
        exit 1
    fi
fi

if [[ -z "${VERSION}" ]]; then
    echo -e "$ERROR_MSG Something has gone wrong, report this error to the administrator."
    exit 2
fi

if [[ ! -f "$CONTENT_FILE" ]]; then
    echo -e "$ERROR_MSG Something has gone wrong, report this error to the administrator."
    exit 2
fi

if [[ ! -d "$BUILD_DIR" ]]; then
    echo -e "$NORMAL_MSG Creating the distribution directory"
    mkdir ${BUILD_DIR}
fi

if [[ -f "${BUILD_DIR}${DIST_FILE}" ]]; then
    echo -e "$WARN_MSG The destination file already exists"

    if [[ ${FORCE} -eq 0 ]]; then
        echo -e "$WARN_MSG Please use the -f option to force the creation of the file"
        exit 1
    else
        echo -e "$NORMAL_MSG Deleting the current file"
        rm ${BUILD_DIR}/${DIST_FILE}
        rm ${BUILD_DIR}/${MD5_FILE}
    fi
fi

echo -e "$NORMAL_MSG Getting the content list"
CONTENT_LIST=
for line in $(cat ${CONTENT_FILE}); do
    CONTENT_LIST="$CONTENT_LIST $line"
done

echo -e "$NORMAL_MSG Patching setup.py"
BUILD_LINE=$(cat setup.py | grep "__build =")
BUILD_VALUE=$(python -c "import subprocess; print(subprocess.check_output('git describe --tags --always HEAD'.split()).decode().strip())")
NEW_BUILD_LINE="__build = '$BUILD_VALUE'"
sed -i "s/${BUILD_LINE}/${NEW_BUILD_LINE}/" setup.py

if [[ "$(cat setup.py | grep "__build =")" != "${NEW_BUILD_LINE}" ]]; then
    echo -e "$ERROR_MSG Couldn't patch setup.py file"
    exit 1
fi

echo -e "$NORMAL_MSG Creating the distribution file"
${TAR_CMD} -czf ${BUILD_DIR}/${DIST_FILE} ${CONTENT_LIST}

RESULT=$?

if [[ "$RESULT" -eq 0 ]]; then
    prev=$(pwd)
    cd ${BUILD_DIR}
    ${MD5_CMD} ${DIST_FILE} > ${MD5_FILE}
    echo -e "$SUCCESS_MSG A new distribution file has been created successfully"
    echo -e "$SUCCESS_MSG Dist file: $BUILD_DIR/$DIST_FILE"
    echo -e "$SUCCESS_MSG MD5 file: $BUILD_DIR/$MD5_FILE"
    cd ${prev}
else
    echo -e "$ERROR_MSG An error occurred while trying to create the distribution file, please check the output messages."
fi

exit ${RESULT}
