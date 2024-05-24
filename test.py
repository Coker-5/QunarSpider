import threading
import requests
import json
import time
import subprocess
from functools import partial
import redis
from urllib3.exceptions import InsecureRequestWarning

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")  # 编码
import execjs

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 取消警告
t = int(round(time.time() * 1000))  # 获取时间戳

#   1.获取cs_june

def getCs_june():
    headers = {
        "authority": "piccolofe.qunar.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://flight.qunar.com",
        "referer": "https://flight.qunar.com/",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62"
    }
    url = "https://piccolofe.qunar.com/fe/tad"
    data = {
        "data": "iKohiK3wy-v0aS30a=D0aS30aS30a2a0aSiSoCX0aS30a=D0aS3nWStsWSDOaKtwaRXwiK3siK3syPLsoAouoCo-yGT+j-oXoOGs9DG9EGoDEPEzXkoqfsH-iK3Aa=EzKAHK9hPwWKihk+WCyIGKaUPwWKihk2LwoAosfwPwWKWDkAW5gO0qa+WQusWsjPezKMGu9CW9u+f+kAW=iK3Aa2iHkkT+jkkOohPwaUPwXwPwaMAxjM0LfPE0oM0SfuPwaUPsX9fHcCW0iKiRiK3wf-fHcGW=gM0bfwPwaUPsXKasiKiRiK3wf-iwEM0wf9fxdhPwaUPsX9fHcCW0iKiRiK3wcIFSj-EQcOm0aS30a=D0aSixywPwaUPwXwPwaMHwf9j0aS30a=D0aSipoCE8gwPsXuPwEUPwEMfLy9opohNno9NHgUNScO=0a2fsy-E0iKiIcON0oOGN-OnQg+E/y9N=f-3byCEeiKWIgOkHgMWpEIk8j-i=o-i0X90wgIFwohPsEhPwWPPNiK3AVKP0aSkhEUPwWPPOiK3AXS30aSPNVuPwW5W0j-iSyDGwgM0Oj9nTy-i8c+i=iKWDiK3AEK20aSkTWUPwWK2OiK3AEKP0aSkhahPwWK2=iK3OgOkHgMWpEIk8j-i=o-i0kI0efuPsER38aSaeaRgeaS20aSfsf9GwjOHTg5iQoMGLkI0efuPsER38aSaeaRteaKt0aSfbf-H=K2EHd-a0a=X8iK3Og+EHg5EKf9GwjOt0a=E=g5k0iK3Of5ixcPWxfIP0a=ERPAt0aSf=c=WxfIP0a=EKEP80aSfMgMFeiKWDg-kbj-iQcME0dhPwWMnxoOksoGTwy9W0iKWDc5kLchPwWMfHoMFwy-E0uOkNiKWDiK3OgOHxoAExoIGLPC30a=Ebo9nLiK3Oj9EAcCEVo9=0a=XniK3OjOHQcIEVo9=0a=X8iK3OjOGUy9NRcIGsgwPsEhPwaUPwXwPwa5EQoIn0iK3wiKWTiK3wiPPsiKt8iK28iPPAiKHGiPihiPPAiK2siPGTiPPAiKt=iPiIiPP+iPiDiK2niPPsiKt8iK2niPPOiK0RiPiTiPP+iPDAiPDmiPPOiK0IiPDAiPPmiPGIiPDwiKiRiPP+iKtNiP3NiPP=iPihiP3+iPPOiK0RiPiTiPP+iPDAiPDmiKiRiPPOiKtNiK2siPPOiKHTiK2miPPNiPDsiK0GiPPOiK0RiPiTiPP+iPDAiPDmqukGWuPmEukhXUkGWuPNawkTXukGWuPmWhkhEUkGWwkhEhPNakGAcMGwqMWxcuPwaUPwXwPwaMe0d-oxgMEsiK3wiKWTiK3wiPPOiK0RiPiTiPP+iPDAiPDmiPPNiKtAiK2wiPPAiPiTiK2+iPPNiPDwiKt=iPPmiPGGiPDwiPPNiPDwiKt=iPPAiPGGiK0TiPPOiKtNiK2siPPOiKHTiK2miPP=iPiRiK2miPPOiKtsiPD8iPP+iKtNiP3NiPP=iPihiP3+iPPOiPGIiK2=iPP=iPihiP3+iKiRiPPOiKtNiK2siPPOiKHTiK2miPPOiK0RiPiTiPP+iPDAiPDmiKiRiPP+iKtNiP3NiPP=iPihiP3+iPPOiK0RiPiTiPP+iPDAiPDmiKiRiPP+iK2=iP3AiPPAiPGDiK28iPPOiK0RiPiTiPP+iPDAiPDmiKiRiPPOiK0RiPiTiPP+iPDAiPDmiPPOiK0IiPDAiPPmiPGIiPDwiKiRiPPmiKtmiPGTiPP+iKHIiPGDiPPOiK0IiPDAiPPmiPGIiPDwiKiRiPPAiK0hiPiDiPPNiK2NiKtAiPPOiK0RiPiTiPP+iPDAiPDmiKiRiPPmiKtniK2=iPP+iPDmiKHhiPPmiKtmiPGTiPP+iKHIiPGDiKiRiPPNiKtAiK2wiPPAiPiTiK2+iPPNiPDwiKt=iPPmiPGGiPDwiKiRiPPAiPGGiPiGiPPNiPDOiKtOiPPNiPDwiKt=iPPmiPGGiPDwiKiRiPPNiKtAiK2wiPPAiPiTiK2+iPPOiKtNiK2siPPOiKHTiK2miKiRiPPNiKtAiK2wiPPAiPiTiK2+iPP=iPihiP3+iPPOiPD8iPiRiKiRiPPNiKtAiK2wiPPAiPiTiK2+iPPAiKHDiK0TiPPAiPGGiPDwiKiRiPPAiK0hiPiDiPPNiK2NiKtAiPPOiK0RiPiTiPP+iPDAiPDmiPPNiPDwiKt=iPPAiPGGiK0TiKiRiPPAiK0hiPiDiPPNiK2NiKtAiPPNiKtAiK2wiPPAiPiTiK2+iPPNiPDwiKt=iPPAiPGGiK0TiKiRP-kbj-3bjOFeiK3wiKiRiK3wfIksj+iQgCEQcOm0aS30a=D0aS30EKP0VDP0X230EKP0VKa0XPD0EKP0VRX0X2jpP-kbj-3bjOFeJukGWhkhEhPNXwkGWhkhVhkhXukGWuPmWukTVhkGWwPNahPmawkGWUPNXwPmahkGWukTWhkTWwkGWwPNXuPmWhkGWhkhVhkTEhkGWUPNWUPmWwkGWUPNWwPmWukGWUkhVhkhVhkGWUPNahPNXwkGWwkhWhkTaUkGWukhXwPNWukGWUPNawPmEuPwXwkGVuPmahPNXukGVhkhEUPmWwkGWukTEUkhVukGWUPNXwkhXukGWwkTWukTVhPwXwkGVuPmWuPNaUkGWukhXuPNWwPwXwkGWUPNWwPmWukGWUkhVhkhVhkGWwkhXukhEUkGVhkhWwkTEUkGWwPNXuPmWhkGWUPNWukhWhkGWuPNahPmVhkGWhkhVhPmEukGWuPmEUPNaukGWukhVhPmawPwXwkGWUPmEUPNahkGWhkhEuPNXUkGWhkhVhPNawkGWhkhVhPNXukGawPmahPmaukGWukTEuPNEukGWUPNWwkhWUkGawPmahPmaukGWuPmEUkTEUkGWhkhEUkTaukGWwPNXuPmWhkGWUPNWwPmWukGWUkhVhkhVhkGWhkhXukTWwkGWuPNawPmaukGWhkhXUkhWwkGWUkTahkhXwkGWUkTEUPNWhkGVhkhEuPmawkGWhkhVhPmEukGWUPNXwPmEhkGWuPmXukTaukGWUkTEUPNWhkGVhkhEuPmawkGWwkhawkhXUkGWwkhXUPNEUPwXwkGWukhVhkTEukGWuPmXukTVukGWUkhWUPmVhkGVhkhWhkhVukGVhPmahPmWukGVhkhEhkhXUkGWUPNEhkhEukGVhkhEUPNXUkGVhkTauPmXwkGWuPmWuPmWukGWuPmVhPmWUkGVuPmahPmVukGWUPmXUkTVuPwXwkGWUPNVhkTEUkGWUPmaUkTVhkGVukTaUPmWhkGVhkTEukTaUkGWUPNXwkhXukGWwkTWukTVhkGawPmahPmaukGVuPmWuPNaUkGWukhXuPNWwkGawPmahPmaukGWUPNWwPmWukGWUkhVhkhVhkGWwkhXukhEUkGVhkhWwkTEUkGWwPNXuPmWhkGWUPNXwPmahkGWhkhEhkhawkGVuPmahPmVukGWUPmXUkTVuD0aS30a2a0aSiAgOkwX9o0c5X0aS30a=D0aSiWc+QQcInHiKiIWum8iK38JGoQcMExo+a0aSTVkhPwaRD8qSv0a=30aST-y9mOWhPsXUPwaCtOWh20aSTTgCTLfko0j2eQohPwESPsWwmsWUPwahHquGEWKhPwXwPwaInQyOP0aSTCf9Wlcw20aSTRyCixc9P0a2jnaKDbahm8qSv0aSTKj9fHgM20a2jAasgbasj0aSTGfIg0a2jnaKDbahmnWSjnqSjwiK3wiKiRiK3wgInHoIfxgM=0aS30a=D0aSi-y9msaUPwaUPwXwPwaME0oM0SfPA0c9FwduPwaUPsXKt0a2a0aSiSgCkRcIGsgwPwaUPsXuPwa5kbyONxoOm0aS30a2a0aSipj-i2oOGwfPWxcMWAg5i0cMWNiK3wiKWTVhPwXwPwaMWxcOeQfPkbj9iLf9X0aS30a=DniKiRiK3wj-T8XOF2fPNHc9P0aS30a=D0aSiWc+QQcInHiK3wiKiRiK3wj-T8KMGefuPwaUPsXuPwa2N0oCWSj-T0iK3wiKiRiK3woOkUfCiQoMkwiK3wiKWTiK3wo9NlcMF+cUPwaUPwXwPwaMExKMF=kCiHjOL0aS30a=D0aSiAcMebc+obiK3wiKiRiK3wcIGbf+kHfOksiK3wiKWTiK3wdMteX=m0a=i0cUPsXMkbqPohiKWhf9mekka0aS30a2a0aSiLj9N5o9G5fuPwaUPsXuPwa5QpqPWViK3wiKiRiK3wgCixfCkSohPwaUPsXuPwa2o0jOexiK3wiKiRiK3woMkbfIFwiK3wiKWTiK3wEOFxfOn0iK38u9NSqUPwaUPwXwPwaMFsj+TAiK3wiKWTiK3wo9NlcMF+cUPwaUPwXwPwaMHQg+Exg50af9N5oIt0aS30a=DwiKiRiK3wc90efkENgIksiK3wiKWTiKkhiK3wPIFwoIGUcIP0aSTDcOWAc9kbohPwaDfxgMAHohPwWMG8gInQjOG=y9FbiKiIgIEMiK3wiKiRiK3wPIFwoIGUcIP0aSTDcOWAc9kbohPwaDfxgMAHohPwW5E0dCX0a2f8fIj0aS30WPX0a2a0aSiHgCT9f-isy9FbiK3wiKWTiK3wWum8iK38JGoQcMExo+a0aSTVkhPwaRD8qSv0a=30aST-y9mOWhPsXUPwaCtOWh20aSTTgCTLfko0j2eQohPwESPsWwmsWUPwahHquGEWKhPwXwPwaInQyOP0aSTCf9Wlcw20aSTRyCixc9P0a2jnaKDbahm8qSv0aSTKj9fHgM20a2jAasgbasj0aSTGfIg0a2jnaKDbahmnWSjnqSjwiK3wiKiRiK3wjOFLc+iDf-T=yhPwaUPsXK3=iKiRiK3wgMkscOnAoI0xcUPwaUPsXuPwaSDAasj0a=3mWSX0aS30a2a0aSiHoMGQcGi0gOFLo-EQcOm0aS30a=D0aS3nWKaOiKWhVR3=iK3wiKiRiK3wfIkOy9W0PI0mf9nuj-EQcwPwaUPsXKDbaSP0a2a0aSiOy9k+gIFwoGWQdMP0aS30a=D0aS3nWRgNiKWhas28iK3wiKiRiK3woO0bfIF+PO0rfuPwaUPsXuPwaSDAasj0a=3maSX0aS30a2a0aSi2jUPwaUPsXKD0a2a0aSiscuPwaUPsXKv0a2a0aSipj-Way9k2PMkscOnAoI0xcUPwaUPsX9fHcCW0iKiRiK3wyIGskO0bfIF+XOHwcOA0iK3wiKWTfMGLgOP0a2a0aSipj-Way9k2X5ixo+W0gUPwaUPsX9fHcCW0iKiRiK3wyIGsKI00fDFsiK3wiKWTfMGLgOP0a2a0aSiso-T8c+i=KIFSj9nKoIFwj9o0iK3wiKWTauPwXwPwa5WAgCTxg5EKf-Wsy9FbP+ExgMG5fuPwaUPsXKD0a2a0aSiso-T8c+i=u9N2f-H0fDEhiK3wiKWTauPwXwPwa5WAgCTxg5ETfIEhf9HHoM0xgUPwaUPsXKv0a2a0aSiso-T8c+i=K+T0c2EHoIGUj-W0iK3wiKWTauPwXwPwa5EQc9krcON0KOfMgOk=iK3wiKWTqKXmahPwXwPwa5EQc9krcON0iK3wiKWTiK3wX-WQjuPwE0Wpj9N5yIGQiK3wiKiRiK3woIFAjOt0aS30a=D0aS38iKWhfMGLgOP0a=iMj9nsfuPwaUPwXwPwa5TLo9oQc5a0aS30a=D0WP30W=30aSibj9A0iK3wiKWTiK3wXOHwcOA0iK3AaSTXEDj0aSPwaGfQf-o0gUPwaUPwXwPwaME0gOWwy-T=y9FbiK3wiKWTiK3wPIFwoIGUcIP0aSPwaDExj+kef9N=iK3AaSTIc+iej-X0aS30a2a0aSiey9A0kC08f-a0aS30a=D0WP30W=30aSi=d-T0iK3wiKWTiK3wj-T8cI0Sj-EQcOm0a2f8fIj0aS30a2a0aSiso9fMy-H0gwPwaUPsXuPwa5T2fUPwaUP+EhPwXwP+XUPwa5ENgIP0aS30a=D0aSi=f-H=iKiIgIEMiK3wiKiRiK3wg+kMfM0mf-a0aS30a=D0aSi8fIj0aS30W=X0WPX0W=X0a2a0W=30aSibj9A0iK3wiKWTiK3wXOHwcOAQo9=0aSPwaGTDEUPwWK38kM00oOkwiK3wiKiRiK3wfIksj+iQgCEQcOm0aS30a=D0aSiXc+i=j9iLfuPwWK38EIFSo9A0c5X0aSPwaDfxgMAHohPwaUPwXwPwaMAQc9kPd-T0gwPwaUPsXuPAXUP+XUPwa5ENgIP0aS30a=D0aSiHgCTLy9WHoI0xcUPwE5T2fUPwaUPwXwPwa5WAfMfQdIksiK3wiKWTiK3wgIEMiK3wiKoDiKiRiKohiK3woC08fuPwaUPsXuPwa5E0dCX0a2f8fIj0aS30a2a0aSiso9fMy-H0gwPwaUPsXuPwa5T2fUPwaUP+EhPAEhP+EhPwXwP+XUPwaMNHc9P0aS30a=D0aSiWy9Wwc+Wxf5X0aSPwaDk2fOP0aSPwaGTDEUPwWK38kM00oOkwiK3wiKiRiK3wfIksj+iQgCEQcOm0aS30a=D0aSiXc+i=j9iLfuPwWK38EIFSo9A0c5X0aSPwaDfxgMAHohPwaUPwXwPwaMAQc9kPd-T0gwPwaUPsXuPAXUP+XUPwa5ENgIP0aS30a=D0aSiHgCTLy9WHoI0xcUPwE5T2fUPwaUPwXwPwa5WAfMfQdIksiK3wiKWTiK3wgIEMiK3wiKoDiKiRiKohiK3woC08fuPwaUPsXuPwa5E0dCX0a2f8fIj0aS30a2a0aSiso9fMy-H0gwPwaUPsXuPwa5T2fUPwaUP+EhPAEhP+EhPwXwP+XUPwaMNHc9P0aS30a=D0aSiXEDj0aSPwaGfQf-o0gUPwaUPwXwPwaME0gOWwy-T=y9FbiK3wiKWTiK3wPIFwoIGUcIP0aSPwaDExj+kef9N=iK3AaSTIc+iej-X0aS30a2a0aSiey9A0kC08f-a0aS30a=D0WP30W=30aSi=d-T0iK3wiKWTiK3wj-T8cI0Sj-EQcOm0a2f8fIj0aS30a2a0aSiso9fMy-H0gwPwaUPsXuPwa5T2fUPwaUP+EhPwXwP+XUPwa5ENgIP0aS30a=D0aSi=f-H=iKiIgIEMiK3wiKiRiK3wg+kMfM0mf-a0aS30a=D0aSi8fIj0aS30W=X0WPX0W=X0a2a0W=30aSibj9A0iK3wiKWTiK3wkOkUuO0=iK3AaSTUo90LohAQcUPwWK38PDEIiK3wiKiRiK3wfIksj+iQgCEQcOm0aS30a=D0aSiXc+i=j9iLfuPwWK38EIFSo9A0c5X0aSPwaDfxgMAHohPwaUPwXwPwaMAQc9kPd-T0gwPwaUPsXuPAXUP+XUPwa5ENgIP0aS30a=D0aSiHgCTLy9WHoI0xcUPwE5T2fUPwaUPwXwPwa5WAfMfQdIksiK3wiKWTiK3wgIEMiK3wiKoDiKiRiKohiK3woC08fuPwaUPsXuPwa5E0dCX0a2f8fIj0aS30a2a0aSiso9fMy-H0gwPwaUPsXuPwa5T2fUPwaUP+EhPAEhP+EhPAEhPwXwPwaMG2XMnxjOL0aS30a=GMj9nsfuPwXwPwa5fQfIkxP+k8iK3wiKWTiKohiK3wcOo5iK3wiKWTiK3wgCixjMGUcC20aS30a2a0aSipaSj=iK3wiKWTiK3wgCixjMGUcC20aS30a2a0aSi+f9ieiK3wiKWTiK3wgCixjMGUcC20aS30W=X0a2a0aSiHo9EQcAWAghPwaUPsXuP+XUPwaMF5fwPwaUPsXuPwa5TwcOiHjMnNiK3wiKiRiK3wc-vsiK3wiKWTiK3wgCixjMGUcC20aS30a2a0aSi+j-j0aS30a=D0aSi8gMFUj9iLduPwaUPwXwPwaM==juPwaUPsXuPwaMAHd9i0iK3wiKoDiKiRiK3wgIkwfMFwc9GbjOP0aS30a=D8qSvNVK2NVK28WRjsaSPOVRaOiKiRiK3wK9FAgOkWc+f0E-f0c5X0aS30a=D0aS30aS30a2a0aSiWc+ksfPExoONGoMkbohPwaUPsXuPwaUPwaUPwXwPwa2Axo-W0K9FOfuPwaUPsXuPwaUPwaUPwXwPwaMo0oDGSoI0xc2EHoIGDj-E0iK3wiKWTiK3wiK3wiKiRiK3wgMkMf-i0gUPwaUPsXuPwaUPwaUPwXwPwaMWxc5WxcIP0aS30a=DniKiRiK3wgIG5fPkLf9A0c5X0aS30a=D0aS30aS30a2a0aSiScOA8cIk=fPWxfIP0aS30a=D0aSiMo9NSoI0xcUPwaG18dIDnVIG2VhtQiKohoMGwiK38-sTmWRgsaSgwiKWDJRTmahPwXA18dRDmfMjmfUPAX018dRkHWS2pisTmVID5JuPAEh2paCtwahPwXsTmaKvQiKWhoMGwiK38-sTmWIPAjOPsiKWD-sTmasgnaSgAiKkhiOE0fMGAcCX5iKkDiKkh-sTmW9DOVut5aCtmjUgQiKkDJRTmaOPmiKiRaCtwWsTMJuPsX5fHgUPwaG18dRX+VKDwjwPsEDEHoIP0WP35cMF+iwPAEhtQiKWhoMGwiK38-sTmaKHHaSjwiKWD-sTmWIPAjOPsiKihiwPwawPwawg0a2i/aCt=WsawWs30a235iK3siK3siwPwX018dRX+VKDwjwPsX5fHgUPwaG18dIDnVIG2VhPsEht8dRv0a2W/aCtAjSj8fR20WPi/aCtAjKjNJhg8dRHHiw20WPXQJDQKK=m0WPi/aCtAjKjNJhg8dRg8iw20WPXp-sTmaKHHaSjwJuPwXA18dREMaRgNjwPAX018dRkHWS2pisTmVID5JuPAEh20a=iwf-EAgMm0aST+y9N2c+g0WPi/aCtAjKjNJhg8dRHSiw20WPXp-sTmjKDmj9XmJuPsXUP+EhPwaUPwXwPwaMW=cwPwaUPsXuPwaUPwaUPwXwPwaMW=cUPwaUPsXuPwaSDOVRaOaKjnVR38WR30aSa0aSWQusW+j-awX9G+PCoHoAT+j-awiK3Aa2ijP+jm9R3sgAoKa+oGPSTujki=o=kX9IN-POGTk+WzcPkD9RH9PRamyPLsgO0qa+WHuOQVjkijgAfqo5o-P+Eek+kXoOGko5X0aS30a2a0aSizo9N0-+j0aS30a=D0aS3nWStsWSDOaKtwaRXwiK3wiKiRiK3woOkUfO80aS30a=D0aS3AjOXwfRPNaKg+WKvmfRXmfSjmjSt8jKgNWOfHWRkMaUPwaUPwXwPwa5o0jMoLaUPwaUPsXuPwa2oxcOoLfuPwaD0bjwm0aSvpu9N=f98Q/2GVE=nGiK38JD0boIkLiKiRiK38u9N=f98pPU20aST3EhPwaDowj-Tpy9WsiK38WSa8iK38EI0wf9W=a=XnauPwaCfs-sk/ahPwaCTs-sk/ahPwXwPwaDXsERDnJuPwaUPwXwPwaMWHc5fHg=fXiK3wiKWTiK3waRDmWMXNWIa=fRtNj9WUWKawaRXNfSfMWMX+WKH2WOX0aS30a2a0aSiMcON=gwPwaUPsXuPwaMXsVIP=V9fMW9DmV9anfIDmVI3mfIGUfIf0aRD+fSPsiK3wiKoD",
        "time": t,
        "lee": "1683616182042",
        "t": "inter_oneway_list_www"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, data=data)
    response.encoding = "utf-8"
    response = response.text
    cs_june = json.loads(response)['data']
    return cs_june


#   2.获取Alina


def get_Alina():
    with open("get_data.js","r",encoding="utf-8") as fp:
        read = fp.read()
    alina = execjs.compile(read).call('w')
    return alina


#   3.获取数据


def get_data(alina, cs_june, ip_pro):
    url = "https://flight.qunar.com/touch/api/inter/wwwsearch"
    print(alina,cs_june)
    header = {
        "cookie":
            "QN1=00008400306c54e01f089d9d;"  

            f"Alina=b36c88ba-601832-724c3a23-76bb4c06-3aa464e57df3;" 

            # 唯一标识
            f"cs_june=ec22b45f0b393155c5368e48e3e18fd21677476e82516c11845bb5e310a5ea17a325113e07265394f81625614b346adaab783c3c6f39c32113517211eae7a1dfb17c80df7eee7c02a9c1a6a5b97c1179864862ea0c944522e253f2fb7de9561b5a737ae180251ef5be23400b098dd8ca",

            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62"
    }
    proxy = {
        'http': "http://" +ip_pro
    }

    params = {
        "depCity": "上海",  # 出发地
        "arrCity": "首尔",  # 到达点
        "depDate": "2023-08-30",    # 出发时间
        "adultNum": 1,
        "childNum": 0,
        "from": "qunarindex",
        "ex_track": "",
        "es": "",
        "_v": 8,
    }

    resp = requests.get(url=url, headers=header, params=params, verify=False)
    resp = resp.text
    print(resp)
    return resp




#   4.解析数据

def exec_data(data):
    try:
        flights = json.loads(data)['result']['flightPrices']
        num = len(flights)  # 航班数量
        for key, value in flights.items():
            flight_name = key  # 航班名称
            lowest_price = value['price']['lowTotalPrice']  # 航班价格
            flight = value['journey']['trips'][0]['flightSegments'][0]
            departure_name = flight['depCityName'] + flight['depAirportName']  # 航班出发点
            departure_time = flight['depDate'] + flight['depTime']  # 航班出发时间
            arr_name = flight['arrCityName'] + flight['arrAirportName']  # 航班到达点
            arr_time = flight['arrDate'] + flight['arrTime']  # 航班到达时间
            gs_name = flight['carrierFullName']  # 所属公司
            flight_type = flight['planeTypeName']  # 航班类型
            flight_seat = value['journey']['seatInfo']['nums']  # 座位信息
            flight_tax = value['price']['tax']  # 航班税
            flight_info_list = []
            flight_data = {
                "flight_num": flight_name,
                "lowest_price": lowest_price,
                "departure_name": departure_name,
                "departure_time": departure_time,
                "arr_name": arr_name,
                "arr_time": arr_time,
                "flight_type": flight_type,
                "flight_seat": flight_seat,
                "flight_tax": flight_tax
            }
            flight_info_list.append(flight_data)
            print(f"航班号：{flight_name} 所属公司：{gs_name} 航班出发点：{departure_name} 航班出发时间：{departure_time} 航班到达点:{arr_name} 航班到达时间：{arr_time} 最低价格：{lowest_price} 机型：{flight_type}")
    except Exception as e:
        print("数据为空！！"+e)


def start(ip_pro):
    cs_june = getCs_june()
    alina = get_Alina()
    data = get_data(alina, cs_june, ip_pro)
    exec_data(data)


if __name__ == '__main__':
    # client = redis.Redis(host="localhost", port=6379, decode_responses=True, db=5)
    # ip_dict = client.keys()
    # ip_dict = client.mget(ip_dict)
    # i = 1
    # for items in ip_dict:
    #     ip_pro = items  # 代理ip地址
    #     thread_item = threading.Thread(target=start, args=(ip_pro,))
    #     thread_item.name = f"线程{i}"
    #     thread_item.start()
    #     i = i+1
    cs_june = getCs_june()
    alina = get_Alina()
    get_data(alina, cs_june,"127.0.0.1")