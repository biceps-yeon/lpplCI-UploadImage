# 위젯용 LPPL CI 이미지 생성

이것은 lppls 모듈을 사용하여 휴대폰 위젯용 KOSPI, S&P500, TESLA의 최근 10년간의 LPPL CI 이미지를 생성, cloudinary에 고정 URL로 업로드하는 프로젝트입니다.
실행환경은 깃허브 액션으로 설정하였고, local 실행도 가능합니다.
![LPPLS Confidnce Indicator of TESLA](https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/TESLA.png)

## Update Status
깃허브 액션 실행 시각 (KST, 화~토 = 전 거래일 장 마감 이후)
 - KR Market (`DailyUpdate_KR.yml`): 03시
 - US Market (`DailyUpdate_US.yaml`): 12시

대상 티커 목록은 `config.py`의 `MarketConfig` 참고

### LPPL CI 계산 캐시
윈도우(끝 날짜 기준)별 nested fit 결과를 `lppl_cache/{name}.npz`에 저장하고, 다음 실행에서는 비어있는 최근 윈도우만 계산합니다.
 - 계산 간격: 캐시 도입 이전 구간은 2거래일(`OUTER_INCREMENT`), 이후 구간은 매일 실행분이 누적되어 1거래일
 - 깃허브 액션: `actions/cache`로 마켓별(`lppl-cache-KR-*`, `lppl-cache-US-*`) 보존. 캐시가 없으면(첫 실행, 7일 이상 미실행으로 삭제 등) 전체 계산
 - 과거 가격이 바뀐 윈도우(액면분할 등)나 `engine/ComputeLPPLCI.py`의 하이퍼파라미터가 바뀐 경우 자동 재계산
 - 강제 전체 재계산: 로컬은 `lppl_cache/` 삭제, 액션은 Actions > Caches에서 해당 캐시 삭제

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
 - `engine/ComputeLPPLCI.py`: LPPLS nested fit 계산 (캐시 기반 증분 계산)
 - `engine/plot_confidence_indicators.py`: 가격 + pos/neg confidence indicator 차트
 - `engine/cloudinary_uploader.py`: 티커별 계산 → 이미지 저장 → Cloudinary 업로드 루프

## Important link
 - lppls module source: https://github.com/Boulder-Investment-Technologies/lppls
