# 위젯용 LPPL CI 이미지 생성

이것 lppls 모듈을 사용하여 휴대폰 위젯용 KOSPI, S&P500, TESLA의 LPPL CI 이미지를 생성, cloudinary에 고정 URL로 업로드하는 프로젝트입니다.
실행환경은 깃허브 액션으로 설정.
![LPPLS Confidnce Indicator of TESLA](https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/TESLA.png)

## 업로드 링크
매주 월요일 9시 업로드
-KOSPI: https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/KOSPI.png
-S&P500: https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/SNP500.png
-TESLA: https://res.cloudinary.com/dx1rb2dye/image/upload/lppls/TESLA.png

## 사용 방법
.env 파일 생성, cloudinary 설정 입력
```bash
#Cloudinary API
CLOUDINARY_CLOUD_NAME= your cloudinary cloud name
CLOUDINARY_API_KEY= your cloudinary api key
CLOUDINARY_API_SECRET= your cloudinary api secret
```

로컬에서 실행할 경우 다음의 문장을 변경 (docstring 해제, cloudinary 깃허브 실행용 삭제)
```bash
    """load_dotenv()""" #현지에서 실행시 실행

....

        """ # Cloudinary 업로드 현지 실행용
        cloudinary.config(
            cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
            api_key = os.environ.get("CLOUDINARY_API_KEY"),
            api_secret = os.environ.get("CLOUDINARY_API_SECRET")
        ) """

        # Cloudinary 업로드 깃허브 액션 실행용
        cloudinary.config(
            cloud_name = os.environ["CLOUDINARY_CLOUD_NAME"],
            api_key = os.environ["CLOUDINARY_API_KEY"],
            api_secret = os.environ["CLOUDINARY_API_SECRET"]
        )
```

terminal에 다음을 입력
```bash
pip install -r requirements.txt
python test_lpplci.py
```

##Important link
-lppls module source: https://github.com/Boulder-Investment-Technologies/lppls
