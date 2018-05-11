#!/bin/bash

ARCHIVE_DIR=/home/cjy/GraduationProject/crawler/crawled_data/daum_news

ARCHIVE_DAYS_DIR=$(find "${ARCHIVE_DIR}"/* -type d)

for ARCHIVES_DIR in ${ARCHIVE_DAYS_DIR}; do
    #echo ${ARCHIVES_DIR##*/}
    DIR_NAME=${ARCHIVES_DIR##*/}
    mkdir -p ./output/${DIR_NAME}
    ./filter.py ${ARCHIVES_DIR} -o ./output/${DIR_NAME}/output.json
    cd ./output/${DIR_NAME}
    python3 ../../process_data.py "output.json" && sed -i '/^$/d' *.txt && ../../seperate_dataset.py title.txt comment.txt
    cd - > /dev/null
done
