from engine.DataLoader import load_data
from engine.ComputeLPPLCI import compute_lpplci
from engine.plot_confidence_indicators import plot_confidence_indicators

import datetime
import cloudinary
import matplotlib.pyplot as plt
from lppls import lppls


def test_cloudinary_upload(tickers):
    uploaded_urls = []

    today = date.today().strftime('%Y%m%d')
    
    for ticker in tickers:
        print(f"--------------------------calculating {ticker['name']}--------------------------")
        # 데이터 로드
        observations, latest_market_date = load_data(ticker['symbol'])

        # LPPLS 계산
        lppls_model, res = compute_lpplci(observations, lppls)

        # confidence indicator 데이터프레임 생성
        res_df = lppls_model.compute_indicators(res)

        # 시각화
        
        plot_confidence_indicators(res, res_df)
        
        fig = plt.gcf()
        fig.subplots_adjust(top=0.83)
        
        fig.suptitle(
            f"{ticker['name']} ({latest_market_date.strftime('%Y-%m-%d')})",
            fontsize=40,
            fontweight='bold',
            y=0.97
        )
        
        latest_pos = float(res_df["pos_conf"].iloc[-1])
        latest_neg = float(res_df["neg_conf"].iloc[-1])
        
        fig.text(
            0.5, 0.90,
            f"LPPL CI  pos={latest_pos:.3f}, neg={latest_neg:.3f}",
            ha='center',
            fontsize=25,
            fontweight='bold'
        )

        plt.savefig(f"{ticker['name']}.png", bbox_inches='tight')
        #plt.show()
        
        upload_result = cloudinary.uploader.upload(
            f"{ticker['name']}.png",
            public_id = f"lppls/{ticker['name']}",
            overwrite=True,
            invalidate=True,
            resource_type="image"
        )
        uploaded_urls.append({
            'name': ticker['name'],
            'symbol': ticker['symbol'],
            'url': upload_result['secure_url']
        })
    
    print("✅ 업로드된 이미지 URL 목록:")
    for item in uploaded_urls:
        print(f"{item['name']} ({item['symbol']}): {item['url']}")