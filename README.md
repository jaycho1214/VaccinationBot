# 코로나 백신 사전예약 봇

**필수**: 크롬 브라우저 및 파이썬이 꼭 설치 되어 있어야 합니다!

**참고**: 휴대폰 본인인증에 있는 자동입력방지 문구와 검사할 곳은 직접 입력하셔야 합니다!

## 사용방법
*파이썬 3.9버전 미만은 작동 여부를 확인하지 않았습니다*

1. `pip3 install -r requirements.txt` 또는
`conda env create -f environment.yml && conda activate VaccinationBot`

2. `target`폴더에 있는 `template.ini`를 본인에 맞게 변경하시면 됩니다. 혹시 여려명을 동시에 할 경우 `template.ini`파일을 복사해서 각각 변경하시면 됩니다.

3. `python3 run_vaccinate.py` 

## Requirements
* [Selenium](https://pypi.org/project/selenium/)
* [chromedriver_autoinstaller](https://pypi.org/project/chromedriver-autoinstaller/)

## 문제제기
이슈나 제안할 점은 여기로 제보해주시기 바랍니다 :)
[이슈 제보하기](https://github.com/MO-Ventures/VaccinationBot/issues)