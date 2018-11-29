# tweet generation을 at job으로 등록하는 관련 스크립트 설명
트윗을 생성하고 업로드 하는 작업에 대한 at job은 'd'큐에 등록한다.
따라서 'd'큐에 있는 at job은 위의 작업에 관련돼 있다고 가정한다.


## enq_generation_at_job.sh
다음 메인 뉴스 중 하나를 선택해 댓글을 생성하고 트윗 하는 작업을 at job 큐에 등록하는 스크립트이다.
위의 작업이 실행될 시각을 입력으로 받는다. 시각은 24시간 표기로 HH:MM 형식으로 입력 받는다.
위의 작업을 입력된 시각으로 하여 'd'큐에 등록한다.

- input : 작업 실행 시각
- output : None

> ~:~/GraduationProject/bin$ ./enq_generation_at_job.sh 17:02

# get_tweet_schedule.sh
'd'큐에 있는 작업들은 위의 작업 관련된 일이라 가정하고 at job 'd'큐에 등록 돼 있는 작업들의 목록을 가져온다.
출력 예시는 다음과 같다.
```
2018 Nov 8 15:30:00 73
2018 Nov 8 19:07:00 74
```
각 줄은 작업 하나를 의미하고 작업이 실행될 년, 월, 일, 시, job number 순으로 출력 된다.

- input : None
- output : 트윗 생성 스케쥴(표준출력)

> ~:~/GraduationProject/bin$ ./get_tweet_schedule.sh

# deq generation at job
스케쥴에서 삭제할 작업이 있는 경우 'atrm'명령어에 job number를 입력으로 넣는다.

- input : job number
- output : None

> ~:~$ atrm 74
