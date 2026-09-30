# -*- coding: utf-8 -*-
"""로컬 실행용 엔트리포인트

사용: python run_local.py [--market KR|US]   (기본값 KR)
Cloudinary 인증 정보는 프로젝트 루트의 .env 파일에서 읽는다.
"""

import argparse
import sys

from dotenv import load_dotenv

from config import MarketConfig
from engine.cloudinary_uploader import configure_cloudinary, run_and_upload

if __name__ == "__main__":
    # Windows 콘솔(cp949)에서 이모지 출력 시 UnicodeEncodeError 방지
    sys.stdout.reconfigure(encoding="utf-8")
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--market", choices=["KR", "US"], default="KR")
    args = parser.parse_args()

    configure_cloudinary()
    run_and_upload(MarketConfig[args.market]["tickers"])
