# 위젯용 LPPL CI 이미지 생성

이것은 lppls 모듈을 사용하여 휴대폰 위젯용 KOSPI, S&P500, TESLA의 최근 10년간의 LPPL CI 이미지를 생성, cloudinary에 고정 URL로 업로드하는 프로젝트입니다.
실행환경은 깃허브 액션으로 설정하였고, local 실행도 가능합니다.
![LPPLS Confidnce Indicator of TESLA](https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/TESLA.png)

## Update Status
깃허브 액션 실행 시각 (KST, 화~토 = 전 거래일 장 마감 이후)
 - KR Market (`DailyUpdate_KR.yml`): 03시
 - US Market (`DailyUpdate_US.yaml`): 12시

대상 티커 목록은 `config.py`의 `MarketConfig` 참고

lppl ci 하이퍼파라미터 각 종목마다 fitting 필요

티커의 종가 시계열을 불러오지 못하는 문제 발생: 260525
해결중

## 업로드 링크
`https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/{name}.png` 형식 (`name`은 `config.py`의 티커 이름)
 - KOSPI: https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/KOSPI.png
 - S&P500: https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/SNP500.png
 - TESLA: https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/TESLA.png

## 사용 방법
로컬에서 실행할 경우 .env 파일 생성, cloudinary 설정 입력
```bash
#Cloudinary API
CLOUDINARY_CLOUD_NAME= your cloudinary cloud name #e.g. CLOUDINARY_CLOUD_NAME= aaaaaaaa
CLOUDINARY_API_KEY= your cloudinary api key #e.g. CLOUDINARY_API_KEY= 1111111
CLOUDINARY_API_SECRET= your cloudinary api secret #e.g. CLOUDINARY_API_SECRET= BBBBBBB
```

requirements.txt 설치 후 run_local.py 실행
```bash
pip install -r requirements.txt
python run_local.py --market KR   # 또는 --market US (기본값 KR)
```

## 파일 구조
 - `run_GithubAction.py`: 깃허브 액션 엔트리포인트 (`--market KR|US`)
 - `run_local.py`: 로컬 엔트리포인트 (.env 로드)
 - `config.py`: 마켓별 티커 목록
 - `engine/DataLoader.py`: yfinance로 최근 10년 종가 로드
 - `engine/ComputeLPPLCI.py`: LPPLS nested fit 계산
 - `engine/plot_confidence_indicators.py`: 가격 + pos/neg confidence indicator 차트
 - `engine/cloudinary_uploader.py`: 티커별 계산 → 이미지 저장 → Cloudinary 업로드 루프

## Important link
 - lppls module source: https://github.com/Boulder-Investment-Technologies/lppls
