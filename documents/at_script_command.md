# at 스크립트
1. 다음 메인 뉴스 가져오기 + 임의의 뉴스 선택
    - input: None
    - output: url, title

2. 뉴스 기사 URL/title 에 대해 charRNN 모델 댓글 생성
    - input: url / text
    - output: comment text

3. 뉴스 기사 URL/title에 대해 NMT 모델 댓글 생성
    - input: url / title
    - output: comment text

4. Twitter 업로드
    - input: text(뉴스제목 + url + charRNN comment + nmt comment)
    - output: None

- 1-4 각각 script로 구현
- 1-4 전 과정 Log 남기기
