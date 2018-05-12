# TweetUploader
## 요구사항
- [python](https://www.python.org/) 3.5 이상
- [python-twitter](https://github.com/bear/python-twitter)
- [tensorflow](https://www.tensorflow.org/) for python
- [Selenium with python](http://selenium-python.readthedocs.io/)
- [geckodriver](https://github.com/mozilla/geckodriver) (PATH에 등록되어있어야 함.)

Thanks To
- [kor-char-rnn-tensorflow](https://github.com/insikk/kor-char-rnn-tensorflow)
## 사용법
트윗을 업로드 하기 위해선 다음 명령어를 실행한다.
```
python3 TweetUploader SAVE_DIR
```
업로드 시간을 구하기 위해서는 디렉토리에 `time_save/` 디렉토리와 `time_generate.py` 모듈이 있어야 한다. 두가지 요구사항은 [dachshu/charRNN](https://github.com/dachshu/charRNN)에서 찾을 수 있다.
## 예시
## TODO
