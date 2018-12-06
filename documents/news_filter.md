# 뉴스 필터 스크립트

이 스크립트는 크롤링 된 JSON 포맷의 뉴스 데이터를 입력 받아서 공감/비공감 비율 순 상위 10%의 댓글만 반환한다. 이 때 비공감 수는 2배가 되어 계산에 사용된다.

## 사용법

```
python3 news_filter.py [INPUT_FILE_OR_DIR] [--dislike_multiplier MUL][-o OUT_FILE]
혹은
./news_filter.py [INPUT_FILE_OR_DIR] [--dislike_multiplier MUL][-o OUT_FILE]
```

INPUT_FILE_OR_DIR : 크롤링 된 뉴스 기사 데이터 파일 또는 그걸 담고 있는 디렉토리를 지정한다. 디렉토리가 주어진 경우 하위 경로를 모두 순회하면서 찾은 모든 파일을 기사 데이터 파일로 취급한다. 이 인자가 주어지지 않은 경우 stdin에서 디렉토리 혹은 파일의 경로들을 읽는다.

## 출력 형식
다음 형태의 JSON 데이터를 stdout으로 출력한다.

```
[
    {
        "title": 뉴스 제목,
        "comments": [
            댓글1,
            댓글2,
            ...
        ]
    },
    ...
]
```