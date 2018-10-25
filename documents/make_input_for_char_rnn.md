# CharRNN용 입력 생성 스크립트
[뉴스 필터 스크립트]의 결과물을 입력으로 받아서 CharRNN 모델이 학습할 input 파일로 변환시키는 스크립트.

## 사용법
```
python3 make_input_for_char_rnn.py INPUT_FILE OUT_DIR
혹은
./make_input_for_char_rnn.py INPUT_FILE OUT_DIR
```

INPUT_FILE : [뉴스 필터 스크립트]가 만들어낸 파일을 지정한다.
OUT_DIR : 출력파일이 저장될 디렉토리. 이 디렉토리 안에 input.txt란 이름으로 파일이 저장된다. 디렉토리가 없다면 생성한다.

## 출력 형식
개행문자를 구분자로 해서 한 줄에 댓글 하나씩 기록된다.

```
기사제목1\t댓글내용1
기사지목1\t댓글내용2
기사제목2\t댓글내용3
...

```

[뉴스 필터 스크립트]:(./news_filter.md)
