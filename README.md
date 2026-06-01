# 위젯용 LPPL CI 이미지 생성

이것은 lppls 모듈을 사용하여 휴대폰 위젯용 KOSPI, S&P500, TESLA의 최근 10년간의 LPPL CI 이미지를 생성, cloudinary에 고정 URL로 업로드하는 프로젝트입니다.
실행환경은 깃허브 액션으로 설정하였고, local 실행도 가능합니다.
![LPPLS Confidnce Indicator of TESLA](https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/TESLA.png)

## Update Status
깃허브 액션 KR Market 00시, US Market 12시 실행

lppl ci 하이퍼파라미터 각 종목마다 fitting 필요

티커의 종가 시계열을 불러오지 못하는 문제 발생: 260525
해결중

## 업로드 링크
주중 오전 04시 업로드
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

requirements.txt 설치 후 test_Local.py 실행

## Important link
 - lppls module source: https://github.com/Boulder-Investment-Technologies/lppls
