# get daum main news script
스크립트 실행 시점 다음(Daum) 모바일 페이지 메인 뉴스 상위 5개 뉴스중 임의로 하나를 선택 해
선택한 뉴스의 제목과 URL을 출력한다
- input : None
- output : 제목 '\n' URL

> ~:~/GraduationProject/bin$ ./get_daum_main_news.sh


# generate charRNN/nmt comment script
입력받은 기사 제목 텍스트를 charRNN/nmt 모델에 입력으로 넣어 댓글 텍스트를 생성한다.
이때 생성한 댓글 텍스트는 '~/GraduationProject/results/TODAY/(title text에 대한 md5sum)_charRNN'
디렉토리 안의 'output.txt'에 저장된다.
스크립트가 동시에 실행되도 기사제목만 다르면 input, output 파일이 충돌하지
않도록 하기 위해 디렉토리 경로에 md5sum 해시 값을 사용했다.

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
- output : 생성한 댓글들이 있는 디렉토리 경로

> ~:~/GraduationProject/bin$ ./generate_comment_tweet.sh
