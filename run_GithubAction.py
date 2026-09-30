# -*- coding: utf-8 -*-
"""GitHub Actions용 엔트리포인트

사용: python run_GithubAction.py --market KR|US
Cloudinary 인증 정보는 워크플로의 secrets(환경변수)로 전달된다.

lppls repo: https://github.com/Boulder-Investment-Technologies/lppls
"""

import argparse

from config import MarketConfig
from engine.cloudinary_uploader import configure_cloudinary, run_and_upload

if __name__ == "__main__":
    # argparse로 market 인자 받기 ("KR" 또는 "US")
    parser = argparse.ArgumentParser()
    parser.add_argument("--market", choices=["KR", "US"], required=True)
    args = parser.parse_args()

    configure_cloudinary()
    run_and_upload(MarketConfig[args.market]["tickers"])
