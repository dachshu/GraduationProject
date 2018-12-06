# Daum News Crawler
다음 뉴스 랭킹중 댓글이 가장 많은 50개의 기사들을 크롤링한다.

수집을 자동화하기 위해 [Selenium](https://www.seleniumhq.org/)을 이용한다. Selenium과 geckodriver를 통해서 Firefox 브라우저를 제어하고 자료를 수집한다.

수집하는 자료는 아래와 같다.
- 기사 제목
- 기사 본문
- 기자 이름
- 기사 작성 시간
- 기사 id (기사의 고유 id로 url에 사용됨.)
- 댓글 작성자
- 댓글 id (댓글 고유 id)
- 댓글 작성 시간
- 댓글 내용
- 추천/비추천 수
- 댓글의 댓글 (id, 내용, 작성자, 작성 시간)

프로그램이 실행되면 크롤링 해야할 기사 url들을 모두 모으고, worker process들을 생성해서 병렬적으로 크롤링한다.

## 요구사항
- [Selenium with Python](http://selenium-python.readthedocs.io/)
- [Firefox](https://www.mozilla.org/firefox/)
- [geckodriver](https://github.com/mozilla/geckodriver)
- [Python 3](https://www.python.org/)

## 사용법
```
python3 DaumCrawler.py date out_dir [-p PROCESS_NUM]
```

* date: 크롤링할 기사들의 날짜를 지정한다. 날짜 포맷은 `yyyymmdd`이다.
* out_dir: 수집된 기사들이 저장될 디렉토리를 지정한다. 이미 존재하는 디렉토리여야 한다.
* -p, --process_num: 크롤링에 사용할 worker process의 수를 지정한다.

## 출력 형식
수집된 기사들이 저장된 디렉토리들을 stdout으로 출력한다.