# TwitterController

Twitter API를 이용해 특정 사용자를 Follow 하거나, 특정 트윗을 Retweet 등 트위터 계정을 제어하는 스크립트

할 수 있는 작업들은 다음과 같다.
* 특정 사용자 Follow/Unfollow
* 특정 계정의 타임라인 가져오기(JSON 형식의 출력)
* 추천 사용자 카테고리 혹은 추천 사용자 가져오기
* 특정 트윗 Retweet

## 사용법

```
python3 TwitterController.py [follow|retweet|timeline|suggest] [options...]
```
### 공통 옵션
* --key KEY_FILE : Twitter API를 사용하기 위한 api key가 담긴 key 파일 경로. 항상 요구되며, 해당 파일에 read permission이 있어야 한다. key 파일의 각 줄엔 다음 토큰 문자열이 있어야 한다.
    1. consumer_key
    2. consumer_secret
    3. access_token_key
    4. access_token_secret
* --help : 도움말을 출력한다.
    
### Follow 옵션
* --user_name, -u NAME : 팔로우할 사용자의 이름. user_name이나 user_id 중 하나는 주어져야 함.
* --user_id ID : 팔로우할 사용자의 식별자(정수). user_name이나 user_id 중 하나는 주어져야 함.
* --unfollow : 사용자를 팔로우 하는 대신 언팔로우 함.

### Retweet 옵션
* TWEET_ID : 리트윗할 트윗 식별자(정수).

### Timeline 옵션
* --user_name, -u NAME : 팔로우할 사용자의 이름. user_name이나 user_id가 주어지지 않으면 자신의 timeline 반환.
* --user_id ID : 팔로우할 사용자의 식별자(정수). user_name이나 user_id가 주어지지 않으면 자신의 timeline 반환.
* --num_status, -n NUM : 가져올 타임라인 최대 트윗 갯수. 200을 넘기면 안됨.

### Suggest 옵션
* --get_category : 추천 카테고리를 가져와 출력한다. 각 카테고리 이름은 한줄에 하나씩 출력된다. --get_user 옵션이 설정된 경우, 아무런 동작도 하지 않는다.
* --from_category CATEGORY : 해당 카테고리의 추천 사용자들을 출력한다. 사용자 이름은 한줄에 하나씩 출력된다.