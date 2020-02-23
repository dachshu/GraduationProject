#!/bin/bash

TIME_LINE="$(/home/cjy/GraduationProject/TwitterController/TwitterController.py home-timeline --key_file /home/cjy/GraduationProject/TwitterController/twitter_key)"

IDS=($(echo "${TIME_LINE}" | cut -d" " -f -1 | xargs -I{} echo "{}"))
#TEXTS=($(echo "${TIME_LINE}" | cut -d" " -f 2- | xargs -I{} echo "{}"))

#i=0
#for ids in ${IDS[@]}
#do
    #echo $ids
    #j=$((i+1))
    #echo ${TEXTS[${i}]}
    #echo ${j}
    #i=$((i+2))
#done

mkdir -p /home/cjy/GraduationProject/results/retweet
TEXTS=$(echo "${TIME_LINE}" | cut -d" " -f 2- | xargs -I{} echo "{}")
i=0
echo "${TEXTS}" | while read text
do
    echo "$text" >  "/home/cjy/GraduationProject/results/retweet/${IDS[$i]}.txt"
    i=$((i+1))
done

find /home/cjy/GraduationProject/crawler/crawled_data/daum_news -type d | sort | tail -3 | /home/cjy/GraduationProject/bin/news_filter.py --out-plain-text --with-time > /home/cjy/GraduationProject/results/retweet/daum_comments.txt


for ids in ${IDS[@]}
do
    mkdir -p /home/cjy/GraduationProject/results/retweet/$ids
    /home/cjy/GraduationProject/bin//bert_testdata_preprocess.py "/home/cjy/GraduationProject/results/retweet/$ids.txt" "/home/cjy/GraduationProject/results/retweet/daum_comments.txt" "/home/cjy/GraduationProject/results/retweet/$ids"
    /home/cjy/GraduationProject/bert/infer_classifier.sh "/home/cjy/GraduationProject/results/retweet/$ids" "/home/cjy/GraduationProject/results/retweet/$ids"
    INFER_RESULT=$(/home/cjy/GraduationProject/bin/score_bert_eval_output.py "/home/cjy/GraduationProject/results/retweet/$ids/test_results.tsv")
    echo "[$(date +"%T")][INFO] User '$ids' is ${INFER_RESULT}% similar to me"
    if ((${INFER_RESULT}>1));then
    python3 /home/cjy/GraduationProject/TwitterController/TwitterController.py --key_file /home/cjy/GraduationProject/TwitterController/twitter_key $ids
    fi
done

rm -r "/home/cjy/GraduationProject/results/retweet"
