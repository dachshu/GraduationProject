# Tweet Crawler
사람의 텍스트를 모방하기 위해선 사람들이 작성한 텍스트들이 필요하다. 이때 대표적인 SNS이며 짧으면서도 의미 있는 텍스트들이 많은 트위터에서 학습 데이터들을 수집했다. Tweet-Crawler는 트위터를 통해 학습에 필요한 데이터들을 모으기 위한 모듈이다.

트위터 웹에 특정 계정의 특정 날짜에 대한 트윗들을 요청해 받은 HTML 텍스트를 분석하여 필요한 텍스트만 뽑아내도록 구현했다. 사용시에는 트위터를 저장을 시작할 날짜를 입력하면 최근 작정한 트윗까지 웹 크롤링을 통해 읽어와 저장할 수 있다. 또한 모듈을 실행시키면 이전에 수집한 트위터 계정들의 최신 트윗들을 자동으로 업데이트 한다.

HTML 문서에서 트윗들을 저장할 때 일단 문서에서 필요한 데이터들을 전부 저장한다. 따라서 학습 모델에 따라 필요한 데이터들을 뽑아 내는 과정을 추가로 구현했다.
## 요구사항
- [python](https://www.python.org/) >= 3.5
- [Selenium with python](http://selenium-python.readthedocs.io/) >= 3.13.0
- [Firefox](https://www.mozilla.org/ko/firefox/)
- [geckodriver](https://github.com/mozilla/geckodriver) (PATH에 등록되어있어야 함.)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) >= 4.6.3
- [click(python module)](https://click.palletsprojects.com/en/7.x/) >= 7.0
## 사용법
```
python3 main.py --help
Usage: main.py [OPTIONS] ACCOUNT

Options:
  -u, --update              Update the account's tweets
  -c, --crawl_from [%Y-%m]  Do crawling from the specified date.
  -f, --filter [text|time]  Filter to this format.
  --help                    Show this message and exit.
```
## 예시
[PresidentVSKim](https://twitter.com/PresidentVSKim)의 계정을 2011년 6월부터 크롤링해서 필터링 한 결과는 아래와 같이 나온다.

- __data_text__
```
"오세후이가 아가 갠찮은거는, '아끼야 잘산다'카능 옛말을 실천할 줄 아능기라. 묵느거부터 아끼야 진짜 아끼는거거등. 그래 아끼야 거 머꼬, 한강에 그  둥둥이 뭐시라꼬 그거도 띠우고 말이다."

바라, 거 황우리. 니 반값 등록금 말을 꺼냈으모 끝까정 밀어부치야지 쪼다 맹키로 뒤로 숨으뿌이 뭐 되노? 백하점 맹키로 등록금을 두배로 올맀다가 반으로 깎아줐으믄 될꺼를..아이고 쪼다 맹키로...

남는 고엽제 있거등 박정희 무덤에다가 좀 뿌리삐라. RT @korksj: RT @korea486: 북한에 건네준 돈 봉투 사건과 고엽제에는 침묵하면서.. http://j.mp/mDZt2W  누가 빨갱이??? http://twitpic.com/5c9w57 

뉴라이타가 머꼬? 니 아직꺼정 담배 피우나? @korea486 또 다른 뉴라이트에게 속지맙시다  (민생경제정책연구소 @peristory)

복날 개잡거등 나한테도 한그륵 보내라이~ 내가 요새 기력이 쪼매 음따. @jdh800518 폭도는 사람이 아니다 미친개다 때려잡아야 한다

말로 제주도 갈라카노? 거제도가 헐~씬 더 조은데. RT @kjysmile: @dogsul 고기자님 이번에 제주도 가셨잖아요 엄마가 첨으로 제주여행 가실건데.. 3박4일로요~ 제가 운전을 못해서 버스나 택시이동할건데... 추천할만한 코스 있으세요?

봉투를 마 비니루로 만들어 가 교회에 팔믄 돈 되겠꾸만. RT @Jong5seon: @dogsul 대다수의 부담을 감수하면서 돈꺼내는 사람을 배려하는 일부교회의 모습이 알흠답네요  이왕 뚫는거 이정도는 뚫어줘야.. http://yfrog.com/gyi5ntjj 

오세후이 자슥, 무상급식 찬반투표하는데 182억 든다꼬? 그 돈이면 지 딸같은 년 500명도 넘게 대학 등록금 댈 돈인데, 자슥 돈 통크게 써제끼네. 지 딸 두 년 등록금에도 뿌라질 뿐 했다카는 허리가 500명분 돈 날리고도 멀쩡할랑가?

조깝데기 이자슥 니 밥은 묵고 댕기나??? RT @korea486 @MBOUTos21cccc:  "딴나라당도 약해 빠졌다. 나를 국회로 보내다오!!!"  RT @tkfjsrks: ... http://dw.am/LZPfI 

재개발을 할라믄 청와대부텀 해야지. 쥐새끼가 집을 다 갉아무가꼬... RT@korea486 @welovehani:  용산은 도시환경정비구역이라 도정법상 보호라도 받는데 명동은 민간재개발이라 법의 보호도 없습니다. tttp://dw.am/LZPiw

맹박이 이 자슥은 노동자 다 때리잡아 뿌믄 누구델꼬 장사할라 카노? 노동자들 조질라꼬 갱찰 특공대 만들었디나???

...
```

- __data_time__
```
1308218507
1308220495
1308221477
1308222374
1308222435
1308222740
1308222896
1308234570
1308234797
1308235890
1308236383
1308236555
1308236816
1308236913
1308237029
1308237254
1308237559
1308238010
1308238194
...
```
## TODO
- [ ] 필요한 데이터를 뽑아낼 때 트윗 텍스트, 작성 시간을 뽑아내는 기능 외에 사진과 같은 멀티미디어 데이터들도 뽑아낼 수 있는 기능 추가
- [ ] 시작일을 입력하지 않으면 자동으로 해당 계정의 가입 날짜를 알아내 시작일로 설정하는 기능 추가
