# 위젯용 LPPL CI 이미지 생성

이것은 lppls 모듈을 사용하여 휴대폰 위젯용 KOSPI, S&P500, TESLA의 최근 10년간의 LPPL CI 이미지를 생성, cloudinary에 고정 URL로 업로드하는 프로젝트입니다.
실행환경은 깃허브 액션으로 설정하였습니다.
![LPPLS Confidnce Indicator of TESLA](https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/TESLA.png)

## Update Status
깃허브 액션 오전 9시 업데이트 기능 테스트중

테스트 완료 후 다음 변경
 - public_id
```bash
        upload_result = cloudinary.uploader.upload(
            f"{ticker['name']}.png",
            public_id = f"lppl/{ticker['name']}",
            overwrite=True,
            invalidate=True,
            resource_type="image"
        )
```
 - fitting window size
```bash
        workers=8,
        window_size=120,
        smallest_window_size=40,
        outer_increment=20,
        inner_increment=20,
        max_searches=25,
```

## 업로드 링크
매주 월요일 오전 9시 업로드
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
