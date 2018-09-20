# 웹 제어툴

## Log

**각 단계 수행 도중 Error가 발생한 경우 Log파일에 Error 메세지 표시**

1. Crawling 시작, 완료 (크롤링 날짜도 포함)  
    전체 기사들 중에 몇개가 완료되었는지 갱신.
2. Filtering 시작, 완료
3. Char-RNN 학습 시작, 완료  
    기존 모델 back-up 할 때 표시.
    Loss, 현재 Step, 전체 Step 표시.
4. NMT 학습 시작, 완료
    Global Step, 전체 Step 표시.
5. 시간 생성 및 결과 (hh:mm:ss 형식으로)
6. 다음 생성 시각
7. 현시각 다음 뉴스 메인 기사들
8. 선택된 뉴스 기사 제목과 URL
9. Char-RNN 생성 결과
10. NMT 생성 결과
11. Twitter Upload 결과 (원문과 140자로 제한한 글 표시)

제어 패널을 통한 스크립트 실행도 Log에 기록되어야 하므로 모든 Log 기록 전에 Log 파일에 Lock을 건다.

## Control

1. Crawling 버튼 - 날짜를 입력 받아서 실행
2. Filtering 버튼 - 날짜와 Char-RNN/NMT 학습 데이터를 출력할 경로를 받아서 실행
3. Training 버튼 - 학습 데이터 경로와 모델을 저장할 경로를 받아서 실행
4. Generation 버튼 - 사용할 모델(Char-RNN/NMT)과 저장된 모델의 경로를 받아서 실행
5. Upload 버튼 - 업로드할 문자열을 받아서 실행. 140자로 자동적으로 제한해서 업로드
