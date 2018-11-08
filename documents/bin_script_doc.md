# get daum main news script
스크립트 실행 시점 다음(Daum) 모바일 페이지 메인 뉴스 상위 5개 뉴스중 임의로 하나를 선택 해
선택한 뉴스의 제목과 URL을 출력한다
- input : None
- output : 제목 '\n' URL

> ~:~/GraduationProject/bin$ ./get_daum_main_news.sh


# generate charRNN/nmt comment script
입력받은 기사 제목 텍스트를 charRNN/nmt 모델에 입력으로 넣어 댓글 텍스트를 생성한다.
이때 생성한 댓글 텍스트는 '~/GraduationProject/results/TODAY/(title text의 첫글자_실행시각)_charRNN[nmt]'
디렉토리 안의 'output.txt'에 저장된다.
(nmt 모델의 경우 도커에서 한국어 글자 인식 문제로 인해'실행시각_nmt'에 저장된다)

- input : 기사제목 텍스트 ( parameter로 입력)
- output : 생성한 댓글이 있는 디렉토리 경로

> ~:~/GraduationProject/bin$ ./generate_charRNN_comment.sh "title text"


> ~:~/GraduationProject/bin$ ./generate_nmt_comment.sh "title text"


# upload tweet script
트위터에 올릴 텍스트를 parameter로 받아 <https://twitter.com/TestTESTJY/>에 업로드한다.
이때 트위터 특성상 140번째 이상의 글자들은 제거된다.

- input : 업로드할 텍스트
- output : None

> ~:~/GraduationProject/bin$ ./upload_tweet.sh "tweet text"

# generate comment tweet script
스크립트 실행 시점의 다음(Daum) 모바일 페이지 메인 뉴스 상위 5개중 임의의 1개를 선택하고
선택한 뉴스 제목에 대한 charRNN, nmt 모델의 댓글을 생성한다.
또한 생성한 댓글들 결과를 트위터에 업로드한다. 각 모델의 댓글들은 개행문자 '/n'으로 구분된다.
댓글 생성 및 트윗 업로드 at job에 이용된다.

- input : None
- output : 생성한 트윗 텍스트가 있는 디렉토리 경로

> ~:~/GraduationProject/bin$ ./generate_comment_tweet.sh

# generate comment tweet with log
위의 'generate_comment_tweet.sh'스크립트의 실행 결과를 표준 출력이 아닌 로그 파일에 저장하는 스크립트이다.
실행 결과 로그는 '~/GraduationProject/log/YYYY-MM-DD/detail/upload_comment_tweet'디렉토리에 저장된다.
로그의 제목은 현재 스크립트가 실행된 시각으로 'HH:MM:SS.log'형식이다.
한 로그 파일안에 다음 메인 뉴스 제목 가져오기, char RNN, nmt 모델로부터 댓글 생성, 트윗 업로드 전 과정의 출력이 저장된다.

- input : None
- output : 로그 파일

> ~:~/GraduationProject/bin$ ./generate_comment_tweet.sh


