# FileRW
## Description
데이터 파일과 로그 파일에 읽고 쓰는 행동을 관리하는 클래스

## Function
1. **get_all_account() -> list(account, last_year, last_month)**  
초기화 함수. tweets 폴더가 존재하는지 확인하고 없으면 만든다.  
존재하는 계정 디렉토리들을 순회하면서 log와 data를 동기화시키고 최종적으로 존재하는 계정 데이터를 튜플 리스트로 반환한다.

2. **sync_between_data_log(data_path, log_path) -> (last_year, last_month)**  
Log에 있는 마지막 기록과 Data를 비교해서 무결성을 검증하는 함수.
Log에 기록되지 않는 트윗은 Data에서 제거한다.  
Data에 기록이 없으면 None을 반환하고, 기록이 있으면 마지막 기록의 year와 month를 반환한다.

3. **write_tweet_list(account, tw_list, year, month)**  
계정과 tweet_list, year, month를 받아서 계정의 data_file과 log_file에 기록한다.

4. **delete_later_tweet(path, time, file=None)**  
data_file 경로 혹은 file_object를 받아서 time 이후의 데이터들을 data_file에서 제거한다.

5. **check_last_month(data_file, log_file, year, month)**  
year, month가 log에 기록된 마지막 year, month와 같은 경우 기록된 data를 제거한다.