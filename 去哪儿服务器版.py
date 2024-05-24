import concurrent
import math
import random
import string
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
t = int(round(time.time() * 1000))
location = 'fake_useragent.json'
from fake_useragent import UserAgent
ua = UserAgent(cache_path=location)
client = redis.Redis(host="localhost", port=6379, db=0)
flights_data = {
    "result": [],
    "need": 0
}

def getCs_june(start_data={}):
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
        "user-agent": str(ua.random)
    }
    url = "https://piccolofe.qunar.com/fe/tad"
    data = {
        "data": "iKohiK3wy-v0aS30a=D0aS30aS30a2a0aSiSoCX0aS30a=D0aS3nWStsWSDOaKtwaRXwiK3siK3syPLsoAouoCo-yGT+j-oXoOGs9DG9EGoDEPEzXkoqfsH-iK3Aa=EzKAHK9hPwWKihk+WCyIGKaUPwWKihk2LwoAosfwPwWKWDkAW5gO0qa+WQusWsjPezKMGu9CW9u+f+kAW=iK3Aa2iHkkT+jkkOohPwaUPwXwPwaMAxjM0LfPE0oM0SfuPwaUPsX9fHcCW0iKiRiK3wf-fHcGW=gM0bfwPwaUPsXKasiKiRiK3wf-iwEM0wf9fxdhPwaUPsX9fHcCW0iKiRiK3wcIFSj-EQcOm0aS30a=D0aSixywPwaUPwXwPwaMHwf9j0aS30a=D0aSipoCE8gwPsXuPwEUPwEMfLy9opohNno9NHgUNScO=0a2fsy-E0iKiIcON0oOGN-OnQg+E/y9N=f-3byCEeiKWIgOkHgMWpEIk8j-i=o-i0X90wgIFwohPsEhPwWPPNiK3AVKP0aSkhEUPwWPPOiK3AXS30aSPNVuPwW5W0j-iSyDGwgM0Oj9nTy-i8c+i=iKWDiK3AEK20aSkTWUPwWK2OiK3AEKP0aSkhahPwWK2=iK3OgOkHgMWpEIk8j-i=o-i0kI0efuPsER38aSaeaRgeaS20aSfsf9GwjOHTg5iQoMGLkI0efuPsER38aSaeaRteaKt0aSfbf-H=K2EHd-a0a=X8iK3Og+EHg5EKf9GwjOt0a=E=g5k0iK3Of5ixcPWxfIP0a=ERPAt0aSf=c=WxfIP0a=EKEP80aSfMgMFeiKWDg-kbj-iQcME0dhPwWMnxoOksoGTwy9W0iKWDc5kLchPwWMfHoMFwy-E0uOkNiKWDiK3OgOHxoAExoIGLPC30a=Ebo9nLiK3Oj9EAcCEVo9=0a=XniK3OjOHQcIEVo9=0a=X8iK3OjOGUy9NRcIGsgwPsEhPwaUPwXwPwa5EQoIn0iK3wiKWTiK3wiPPsiKt8iK28iPPAiKHGiPihiPPAiK2siPGTiPPAiKt=iPiIiPP+iPiDiK2niPPsiKt8iK2niPPOiK0RiPiTiPP+iPDAiPDmiPPOiK0IiPDAiPPmiPGIiPDwiKiRiPP+iKtNiP3NiPP=iPihiP3+iPPOiK0RiPiTiPP+iPDAiPDmiKiRiPPOiKtNiK2siPPOiKHTiK2miPPNiPDsiK0GiPPOiK0RiPiTiPP+iPDAiPDmqukGWuPmEukhXUkGWuPNawkTXukGWuPmWhkhEUkGWwkhEhPNakGAcMGwqMWxcuPwaUPwXwPwaMe0d-oxgMEsiK3wiKWTiK3wiPPOiK0RiPiTiPP+iPDAiPDmiPPNiKtAiK2wiPPAiPiTiK2+iPPNiPDwiKt=iPPmiPGGiPDwiPPNiPDwiKt=iPPAiPGGiK0TiPPOiKtNiK2siPPOiKHTiK2miPP=iPiRiK2miPPOiKtsiPD8iPP+iKtNiP3NiPP=iPihiP3+iPPOiPGIiK2=iPP=iPihiP3+iKiRiPPOiKtNiK2siPPOiKHTiK2miPPOiK0RiPiTiPP+iPDAiPDmiKiRiPP+iKtNiP3NiPP=iPihiP3+iPPOiK0RiPiTiPP+iPDAiPDmiKiRiPP+iK2=iP3AiPPAiPGDiK28iPPOiK0RiPiTiPP+iPDAiPDmiKiRiPPOiK0RiPiTiPP+iPDAiPDmiPPOiK0IiPDAiPPmiPGIiPDwiKiRiPPmiKtmiPGTiPP+iKHIiPGDiPPOiK0IiPDAiPPmiPGIiPDwiKiRiPPAiK0hiPiDiPPNiK2NiKtAiPPOiK0RiPiTiPP+iPDAiPDmiKiRiPPmiKtniK2=iPP+iPDmiKHhiPPmiKtmiPGTiPP+iKHIiPGDiKiRiPPNiKtAiK2wiPPAiPiTiK2+iPPNiPDwiKt=iPPmiPGGiPDwiKiRiPPAiPGGiPiGiPPNiPDOiKtOiPPNiPDwiKt=iPPmiPGGiPDwiKiRiPPNiKtAiK2wiPPAiPiTiK2+iPPOiKtNiK2siPPOiKHTiK2miKiRiPPNiKtAiK2wiPPAiPiTiK2+iPP=iPihiP3+iPPOiPD8iPiRiKiRiPPNiKtAiK2wiPPAiPiTiK2+iPPAiKHDiK0TiPPAiPGGiPDwiKiRiPPAiK0hiPiDiPPNiK2NiKtAiPPOiK0RiPiTiPP+iPDAiPDmiPPNiPDwiKt=iPPAiPGGiK0TiKiRiPPAiK0hiPiDiPPNiK2NiKtAiPPNiKtAiK2wiPPAiPiTiK2+iPPNiPDwiKt=iPPAiPGGiK0TiKiRP-kbj-3bjOFeiK3wiKiRiK3wfIksj+iQgCEQcOm0aS30a=D0aS30EKP0VDP0X230EKP0VKa0XPD0EKP0VRX0X2jpP-kbj-3bjOFeJukGWhkhEhPNXwkGWhkhVhkhXukGWuPmWukTVhkGWwPNahPmawkGWUPNXwPmahkGWukTWhkTWwkGWwPNXuPmWhkGWhkhVhkTEhkGWUPNWUPmWwkGWUPNWwPmWukGWUkhVhkhVhkGWUPNahPNXwkGWwkhWhkTaUkGWukhXwPNWukGWUPNawPmEuPwXwkGVuPmahPNXukGVhkhEUPmWwkGWukTEUkhVukGWUPNXwkhXukGWwkTWukTVhPwXwkGVuPmWuPNaUkGWukhXuPNWwPwXwkGWUPNWwPmWukGWUkhVhkhVhkGWwkhXukhEUkGVhkhWwkTEUkGWwPNXuPmWhkGWUPNWukhWhkGWuPNahPmVhkGWhkhVhPmEukGWuPmEUPNaukGWukhVhPmawPwXwkGWUPmEUPNahkGWhkhEuPNXUkGWhkhVhPNawkGWhkhVhPNXukGawPmahPmaukGWukTEuPNEukGWUPNWwkhWUkGawPmahPmaukGWuPmEUkTEUkGWhkhEUkTaukGWwPNXuPmWhkGWUPNWwPmWukGWUkhVhkhVhkGWhkhXukTWwkGWuPNawPmaukGWhkhXUkhWwkGWUkTahkhXwkGWUkTEUPNWhkGVhkhEuPmawkGWhkhVhPmEukGWUPNXwPmEhkGWuPmXukTaukGWUkTEUPNWhkGVhkhEuPmawkGWwkhawkhXUkGWwkhXUPNEUPwXwkGWukhVhkTEukGWuPmXukTVukGWUkhWUPmVhkGVhkhWhkhVukGVhPmahPmWukGVhkhEhkhXUkGWUPNEhkhEukGVhkhEUPNXUkGVhkTauPmXwkGWuPmWuPmWukGWuPmVhPmWUkGVuPmahPmVukGWUPmXUkTVuPwXwkGWUPNVhkTEUkGWUPmaUkTVhkGVukTaUPmWhkGVhkTEukTaUkGWUPNXwkhXukGWwkTWukTVhkGawPmahPmaukGVuPmWuPNaUkGWukhXuPNWwkGawPmahPmaukGWUPNWwPmWukGWUkhVhkhVhkGWwkhXukhEUkGVhkhWwkTEUkGWwPNXuPmWhkGWUPNXwPmahkGWhkhEhkhawkGVuPmahPmVukGWUPmXUkTVuD0aS30a2a0aSiAgOkwX9o0c5X0aS30a=D0aSiWc+QQcInHiKiIWum8iK38JGoQcMExo+a0aSTVkhPwaRD8qSv0a=30aST-y9mOWhPsXUPwaCtOWh20aSTTgCTLfko0j2eQohPwESPsWwmsWUPwahHquGEWKhPwXwPwaInQyOP0aSTCf9Wlcw20aSTRyCixc9P0a2jnaKDbahm8qSv0aSTKj9fHgM20a2jAasgbasj0aSTGfIg0a2jnaKDbahmnWSjnqSjwiK3wiKiRiK3wgInHoIfxgM=0aS30a=D0aSi-y9msaUPwaUPwXwPwaME0oM0SfPA0c9FwduPwaUPsXKt0a2a0aSiSgCkRcIGsgwPwaUPsXuPwa5kbyONxoOm0aS30a2a0aSipj-i2oOGwfPWxcMWAg5i0cMWNiK3wiKWTVhPwXwPwaMWxcOeQfPkbj9iLf9X0aS30a=DniKiRiK3wj-T8XOF2fPNHc9P0aS30a=D0aSiWc+QQcInHiK3wiKiRiK3wj-T8KMGefuPwaUPsXuPwa2N0oCWSj-T0iK3wiKiRiK3woOkUfCiQoMkwiK3wiKWTiK3wo9NlcMF+cUPwaUPwXwPwaMExKMF=kCiHjOL0aS30a=D0aSiAcMebc+obiK3wiKiRiK3wcIGbf+kHfOksiK3wiKWTiK3wdMteX=m0a=i0cUPsXMkbqPohiKWhf9mekka0aS30a2a0aSiLj9N5o9G5fuPwaUPsXuPwa5QpqPWViK3wiKiRiK3wgCixfCkSohPwaUPsXuPwa2o0jOexiK3wiKiRiK3woMkbfIFwiK3wiKWTiK3wEOFxfOn0iK38u9NSqUPwaUPwXwPwaMFsj+TAiK3wiKWTiK3wo9NlcMF+cUPwaUPwXwPwaMHQg+Exg50af9N5oIt0aS30a=DwiKiRiK3wc90efkENgIksiK3wiKWTiKkhiK3wPIFwoIGUcIP0aSTDcOWAc9kbohPwaDfxgMAHohPwWMG8gInQjOG=y9FbiKiIgIEMiK3wiKiRiK3wPIFwoIGUcIP0aSTDcOWAc9kbohPwaDfxgMAHohPwW5E0dCX0a2f8fIj0aS30WPX0a2a0aSiHgCT9f-isy9FbiK3wiKWTiK3wWum8iK38JGoQcMExo+a0aSTVkhPwaRD8qSv0a=30aST-y9mOWhPsXUPwaCtOWh20aSTTgCTLfko0j2eQohPwESPsWwmsWUPwahHquGEWKhPwXwPwaInQyOP0aSTCf9Wlcw20aSTRyCixc9P0a2jnaKDbahm8qSv0aSTKj9fHgM20a2jAasgbasj0aSTGfIg0a2jnaKDbahmnWSjnqSjwiK3wiKiRiK3wjOFLc+iDf-T=yhPwaUPsXK3=iKiRiK3wgMkscOnAoI0xcUPwaUPsXuPwaSDAasj0a=3mWSX0aS30a2a0aSiHoMGQcGi0gOFLo-EQcOm0aS30a=D0aS3nWKaOiKWhVR3=iK3wiKiRiK3wfIkOy9W0PI0mf9nuj-EQcwPwaUPsXKDbaSP0a2a0aSiOy9k+gIFwoGWQdMP0aS30a=D0aS3nWRgNiKWhas28iK3wiKiRiK3woO0bfIF+PO0rfuPwaUPsXuPwaSDAasj0a=3maSX0aS30a2a0aSi2jUPwaUPsXKD0a2a0aSiscuPwaUPsXKv0a2a0aSipj-Way9k2PMkscOnAoI0xcUPwaUPsX9fHcCW0iKiRiK3wyIGskO0bfIF+XOHwcOA0iK3wiKWTfMGLgOP0a2a0aSipj-Way9k2X5ixo+W0gUPwaUPsX9fHcCW0iKiRiK3wyIGsKI00fDFsiK3wiKWTfMGLgOP0a2a0aSiso-T8c+i=KIFSj9nKoIFwj9o0iK3wiKWTauPwXwPwa5WAgCTxg5EKf-Wsy9FbP+ExgMG5fuPwaUPsXKD0a2a0aSiso-T8c+i=u9N2f-H0fDEhiK3wiKWTauPwXwPwa5WAgCTxg5ETfIEhf9HHoM0xgUPwaUPsXKv0a2a0aSiso-T8c+i=K+T0c2EHoIGUj-W0iK3wiKWTauPwXwPwa5EQc9krcON0KOfMgOk=iK3wiKWTqKXmahPwXwPwa5EQc9krcON0iK3wiKWTiK3wX-WQjuPwE0Wpj9N5yIGQiK3wiKiRiK3woIFAjOt0aS30a=D0aS38iKWhfMGLgOP0a=iMj9nsfuPwaUPwXwPwa5TLo9oQc5a0aS30a=D0WP30W=30aSibj9A0iK3wiKWTiK3wXOHwcOA0iK3AaSTXEDj0aSPwaGfQf-o0gUPwaUPwXwPwaME0gOWwy-T=y9FbiK3wiKWTiK3wPIFwoIGUcIP0aSPwaDExj+kef9N=iK3AaSTIc+iej-X0aS30a2a0aSiey9A0kC08f-a0aS30a=D0WP30W=30aSi=d-T0iK3wiKWTiK3wj-T8cI0Sj-EQcOm0a2f8fIj0aS30a2a0aSiso9fMy-H0gwPwaUPsXuPwa5T2fUPwaUP+EhPwXwP+XUPwa5ENgIP0aS30a=D0aSi=f-H=iKiIgIEMiK3wiKiRiK3wg+kMfM0mf-a0aS30a=D0aSi8fIj0aS30W=X0WPX0W=X0a2a0W=30aSibj9A0iK3wiKWTiK3wXOHwcOAQo9=0aSPwaGTDEUPwWK38kM00oOkwiK3wiKiRiK3wfIksj+iQgCEQcOm0aS30a=D0aSiXc+i=j9iLfuPwWK38EIFSo9A0c5X0aSPwaDfxgMAHohPwaUPwXwPwaMAQc9kPd-T0gwPwaUPsXuPAXUP+XUPwa5ENgIP0aS30a=D0aSiHgCTLy9WHoI0xcUPwE5T2fUPwaUPwXwPwa5WAfMfQdIksiK3wiKWTiK3wgIEMiK3wiKoDiKiRiKohiK3woC08fuPwaUPsXuPwa5E0dCX0a2f8fIj0aS30a2a0aSiso9fMy-H0gwPwaUPsXuPwa5T2fUPwaUP+EhPAEhP+EhPwXwP+XUPwaMNHc9P0aS30a=D0aSiWy9Wwc+Wxf5X0aSPwaDk2fOP0aSPwaGTDEUPwWK38kM00oOkwiK3wiKiRiK3wfIksj+iQgCEQcOm0aS30a=D0aSiXc+i=j9iLfuPwWK38EIFSo9A0c5X0aSPwaDfxgMAHohPwaUPwXwPwaMAQc9kPd-T0gwPwaUPsXuPAXUP+XUPwa5ENgIP0aS30a=D0aSiHgCTLy9WHoI0xcUPwE5T2fUPwaUPwXwPwa5WAfMfQdIksiK3wiKWTiK3wgIEMiK3wiKoDiKiRiKohiK3woC08fuPwaUPsXuPwa5E0dCX0a2f8fIj0aS30a2a0aSiso9fMy-H0gwPwaUPsXuPwa5T2fUPwaUP+EhPAEhP+EhPwXwP+XUPwaMNHc9P0aS30a=D0aSiXEDj0aSPwaGfQf-o0gUPwaUPwXwPwaME0gOWwy-T=y9FbiK3wiKWTiK3wPIFwoIGUcIP0aSPwaDExj+kef9N=iK3AaSTIc+iej-X0aS30a2a0aSiey9A0kC08f-a0aS30a=D0WP30W=30aSi=d-T0iK3wiKWTiK3wj-T8cI0Sj-EQcOm0a2f8fIj0aS30a2a0aSiso9fMy-H0gwPwaUPsXuPwa5T2fUPwaUP+EhPwXwP+XUPwa5ENgIP0aS30a=D0aSi=f-H=iKiIgIEMiK3wiKiRiK3wg+kMfM0mf-a0aS30a=D0aSi8fIj0aS30W=X0WPX0W=X0a2a0W=30aSibj9A0iK3wiKWTiK3wkOkUuO0=iK3AaSTUo90LohAQcUPwWK38PDEIiK3wiKiRiK3wfIksj+iQgCEQcOm0aS30a=D0aSiXc+i=j9iLfuPwWK38EIFSo9A0c5X0aSPwaDfxgMAHohPwaUPwXwPwaMAQc9kPd-T0gwPwaUPsXuPAXUP+XUPwa5ENgIP0aS30a=D0aSiHgCTLy9WHoI0xcUPwE5T2fUPwaUPwXwPwa5WAfMfQdIksiK3wiKWTiK3wgIEMiK3wiKoDiKiRiKohiK3woC08fuPwaUPsXuPwa5E0dCX0a2f8fIj0aS30a2a0aSiso9fMy-H0gwPwaUPsXuPwa5T2fUPwaUP+EhPAEhP+EhPAEhPwXwPwaMG2XMnxjOL0aS30a=GMj9nsfuPwXwPwa5fQfIkxP+k8iK3wiKWTiKohiK3wcOo5iK3wiKWTiK3wgCixjMGUcC20aS30a2a0aSipaSj=iK3wiKWTiK3wgCixjMGUcC20aS30a2a0aSi+f9ieiK3wiKWTiK3wgCixjMGUcC20aS30W=X0a2a0aSiHo9EQcAWAghPwaUPsXuP+XUPwaMF5fwPwaUPsXuPwa5TwcOiHjMnNiK3wiKiRiK3wc-vsiK3wiKWTiK3wgCixjMGUcC20aS30a2a0aSi+j-j0aS30a=D0aSi8gMFUj9iLduPwaUPwXwPwaM==juPwaUPsXuPwaMAHd9i0iK3wiKoDiKiRiK3wgIkwfMFwc9GbjOP0aS30a=D8qSvNVK2NVK28WRjsaSPOVRaOiKiRiK3wK9FAgOkWc+f0E-f0c5X0aS30a=D0aS30aS30a2a0aSiWc+ksfPExoONGoMkbohPwaUPsXuPwaUPwaUPwXwPwa2Axo-W0K9FOfuPwaUPsXuPwaUPwaUPwXwPwaMo0oDGSoI0xc2EHoIGDj-E0iK3wiKWTiK3wiK3wiKiRiK3wgMkMf-i0gUPwaUPsXuPwaUPwaUPwXwPwaMWxc5WxcIP0aS30a=DniKiRiK3wgIG5fPkLf9A0c5X0aS30a=D0aS30aS30a2a0aSiScOA8cIk=fPWxfIP0aS30a=D0aSiMo9NSoI0xcUPwaG18dIDnVIG2VhtQiKohoMGwiK38-sTmWRgsaSgwiKWDJRTmahPwXA18dRDmfMjmfUPAX018dRkHWS2pisTmVID5JuPAEh2paCtwahPwXsTmaKvQiKWhoMGwiK38-sTmWIPAjOPsiKWD-sTmasgnaSgAiKkhiOE0fMGAcCX5iKkDiKkh-sTmW9DOVut5aCtmjUgQiKkDJRTmaOPmiKiRaCtwWsTMJuPsX5fHgUPwaG18dRX+VKDwjwPsEDEHoIP0WP35cMF+iwPAEhtQiKWhoMGwiK38-sTmaKHHaSjwiKWD-sTmWIPAjOPsiKihiwPwawPwawg0a2i/aCt=WsawWs30a235iK3siK3siwPwX018dRX+VKDwjwPsX5fHgUPwaG18dIDnVIG2VhPsEht8dRv0a2W/aCtAjSj8fR20WPi/aCtAjKjNJhg8dRHHiw20WPXQJDQKK=m0WPi/aCtAjKjNJhg8dRg8iw20WPXp-sTmaKHHaSjwJuPwXA18dREMaRgNjwPAX018dRkHWS2pisTmVID5JuPAEh20a=iwf-EAgMm0aST+y9N2c+g0WPi/aCtAjKjNJhg8dRHSiw20WPXp-sTmjKDmj9XmJuPsXUP+EhPwaUPwXwPwaMW=cwPwaUPsXuPwaUPwaUPwXwPwaMW=cUPwaUPsXuPwaSDOVRaOaKjnVR38WR30aSa0aSWQusW+j-awX9G+PCoHoAT+j-awiK3Aa2ijP+jm9R3sgAoKa+oGPSTujki=o=kX9IN-POGTk+WzcPkD9RH9PRamyPLsgO0qa+WHuOQVjkijgAfqo5o-P+Eek+kXoOGko5X0aS30a2a0aSizo9N0-+j0aS30a=D0aS3nWStsWSDOaKtwaRXwiK3wiKiRiK3woOkUfO80aS30a=D0aS3AjOXwfRPNaKg+WKvmfRXmfSjmjSt8jKgNWOfHWRkMaUPwaUPwXwPwa5o0jMoLaUPwaUPsXuPwa2oxcOoLfuPwaD0bjwm0aSvpu9N=f98Q/2GVE=nGiK38JD0boIkLiKiRiK38u9N=f98pPU20aST3EhPwaDowj-Tpy9WsiK38WSa8iK38EI0wf9W=a=XnauPwaCfs-sk/ahPwaCTs-sk/ahPwXwPwaDXsERDnJuPwaUPwXwPwaMWHc5fHg=fXiK3wiKWTiK3waRDmWMXNWIa=fRtNj9WUWKawaRXNfSfMWMX+WKH2WOX0aS30a2a0aSiMcON=gwPwaUPsXuPwaMXsVIP=V9fMW9DmV9anfIDmVI3mfIGUfIf0aRD+fSPsiK3wiKoD",
        "time": t,
        "lee": "1683616182042",
        "t": "inter_oneway_list_www"
    }
    data = json.dumps(data, separators=(',', ':'))
    try:
        if start_data.get('proxy') is None:
            pro_ip = 'null'
        else:
            pro_ip = str(start_data['proxy'])
        if pro_ip != 'null':
            response = requests.get(url=url, headers=headers, data=data, verify=False,
                                    proxies={'http': 'http://' + str(pro_ip)}, timeout=18)
        else:
            response = requests.get(url=url, headers=headers, data=data, verify=False,
                                    timeout=18)
        response.encoding = "utf-8"
        if response.status_code == 200 or response.status_code == 201:
            response = response.text
            cs_june = json.loads(response)['data']
            return {'cs_june': cs_june}
        else:
            return {'error': f"获取cs_june状态码错误，{response.status_code}"}
    except Exception as e:
        return {'error': f"get cs_june Error,{e}"}


def get_Alina():
    try:
        with open("get_data.js", "r", encoding="utf-8") as fp:
            read = fp.read()
        alina = execjs.compile(read).call('w')
        return {'alina': alina}
    except Exception as e:
        return {'error': f"get_Alina Error,{e}"}


def get_QN1(start_data={}):
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
        "user-agent": str(ua.random)
    }
    characters = list(string.ascii_lowercase + string.digits)
    random.shuffle(characters)
    random_data = '0000' + ''.join(characters[:4]) + ''.join(characters[4:24])
    url = "https://pwapp.qunar.com/api/log/commonLog"
    params = {
        "pt": "www"
    }
    data = {
        "action": [
            {
                "operType": "show",
                "pageUrl": "https://flight.qunar.com/site/oneway_list_inter.htm",
                "operTime": t
            }
        ]
    }
    get_cookies = {
        "QN1": f"{random_data}"
    }
    data = json.dumps(data, separators=(',', ':'))
    if start_data.get('proxy') is None:
        pro_ip = 'null'
    else:
        pro_ip = str(start_data['proxy'])
    try:
        if pro_ip != 'null':
            response = requests.post(url=url, headers=headers, cookies=get_cookies, data=data, params=params, verify=False,
                                    proxies={'http': 'http://' + str(pro_ip)}, timeout=18)
        else:
            response = requests.post(url=url, headers=headers, cookies=get_cookies, data=data, params=params, verify=False,
                                    timeout=18)
        response.encoding = "utf-8"
        if response.status_code == 200 or response.status_code == 201:
            time.sleep(6)
            return {'qn1': random_data}
        else:
            return {'error': f"获取QN1状态码错误，{response.status_code}"}
    except Exception as e:
        return {'error': f"get_QN1 Error,{e}"}


def proxy_ip():
    while True:
        time.sleep(random.uniform(0.02, 0.04))
        try:
            key_name = client.randomkey()
            cd_data_redis = client.get(key_name)
            cd_data = str(cd_data_redis.decode())
            break
        except Exception as e:
            print('jiuyuan IP redis:%s' % str(e), flush=True)
    return str(cd_data)


def convert(code):
    headers = {
        "user-agent": str(ua.random)
    }
    url = "https://www.qunar.com/suggest/livesearch2.jsp"
    params = {
        "lang": "zh",
        "q": code,
        "sa": "true",
        "ver": "1"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200 or response.status_code == 201:
            city_name = response.json()['result'][0]['key']
            return {'city_name': city_name}
        else:
            return {'error': f"三字码转换状态码错误，{response.status_code}"}
    except Exception as e:
        return {'error': f"convert Error,{e}"}


def get_data(cookie, start_data):
    dep_air = convert(start_data['from'])
    arr_air = convert(start_data['to'])
    if dep_air.get('error') is None and arr_air.get('error') is None:
        url = "https://flight.qunar.com/touch/api/inter/wwwsearch"
        header = {
            "user-agent": str(ua.random),
            "cookie": str(cookie)
        }
        params = {
            "depCity": dep_air['city_name'],
            "arrCity": arr_air['city_name'],
            "depDate": start_data['daytime'],
            "adultNum": start_data['adt_num'],
            "childNum": 0,
            "from": "qunarindex",
            "ex_track": "",
            "es": "",
            "_v": 8,
        }
        if start_data.get('proxy') is None:
            pro_ip = 'null'
        else:
            pro_ip = str(start_data['proxy'])
        try:
            if pro_ip != 'null':
                response = requests.get(url=url, headers=header, params=params, verify=False,
                                    proxies={'http': 'http://' + str(pro_ip)}, timeout=18)
            else:
                response = requests.get(url=url, headers=header, params=params, verify=False,
                                    timeout=18)
            response.encoding = "utf-8"

            if response.status_code == 200 or response.status_code == 201:
                resp = json.loads(response.text)
                if resp['status'] != -1:
                    if resp.get('code') != -1 or resp.get('code') is None and resp.get("['result']['flightPrices']") != {}: # 假数据
                        print(f"{pro_ip}请求成功")
                        return {'data': response.text}
                    else:
                        time.sleep(5)
                        response = requests.get(url=url, headers=header, params=params, verify=False,
                                                proxies={'http': 'http://' + str(pro_ip)}, timeout=18)
                        resp = json.loads(response.text)
                        if resp.get('code') != -1 or resp.get('code') is None and resp.get(
                                "['result']['flightPrices']") != {}:
                            print(f"{pro_ip}请求成功")
                            return {'data': response.text}
                        else:
                            time.sleep(5)
                            response = requests.get(url=url, headers=header, params=params, verify=False,
                                                    proxies={'http': 'http://' + str(pro_ip)}, timeout=18)
                            resp = json.loads(response.text)
                            if resp.get('code') != -1 or resp.get('code') is None and resp.get(
                                    "['result']['flightPrices']") != {}:
                                print(f"{pro_ip}请求成功")
                                return {'data': response.text}
                            else:
                                return {'error': f"{pro_ip}出现故障，三次请求仍未成功"}
                else:
                    time.sleep(5)
                    response = requests.get(url=url, headers=header, params=params, verify=False,
                                            proxies={'http': 'http://' + str(pro_ip)}, timeout=18)
                    resp = json.loads(response.text)
                    if resp['status'] != -1:
                        if resp.get('code') != -1 or resp.get('code') is None and resp.get(
                                "['result']['flightPrices']") != {}:
                            print(f"{pro_ip}请求成功")
                            return {'data': response.text}
                        else:
                            return {'error': f"{pro_ip}出现故障，三次请求仍未成功"}
                    else:
                        return {'error': f"{pro_ip}两次请求航班数据为空"}
            else:
                return {'error': f'状态码出错, {response.status_code}'}
        except Exception as e:
            return {'error': f'get_data Error,{e}'}
    else:
        return {'error': dep_air['error']+arr_air['error']}


def exec_data(data):
    try:
        flights = json.loads(data)['result']['flightPrices']
        for key, value in flights.items():
            flight_name = key  # 航班名称
            lowest_price = value['price']['lowPrice']  # 航班基础价格
            flight = value['journey']['trips'][0]['flightSegments'][0]
            stop_cities = ""    # 停靠点
            if value['journey']['nonStopTransferAirports'] != []:
                stop_cities = value['journey']['trips'][0]['transInfos'][0]['cityName']
                flight0 = value['journey']['trips'][0]['flightSegments'][0]
                flight1 = value['journey']['trips'][0]['flightSegments'][1]
                departure_name = flight0['depAirportCode']  # 航班出发点
                arr_name = flight1['arrAirportCode']  # 航班到达点
                departure_time = flight0['depDate'] + " " + flight['depTime']  # 航班出发时间
                departure_time = departure_time.replace("-", "").replace(":", "")
                departure_time = departure_time.replace(" ", "")
                arr_time = flight1['arrDate'] + " " + flight['arrTime']  # 航班到达时间
                arr_time = arr_time.replace(" ", "")
                arr_time = arr_time.replace("-", "").replace(":", "")

            else:
                stop_cities = ""
                departure_name = flight['depAirportCode']  # 航班出发点
                arr_name = flight['arrAirportCode']  # 航班到达点
                departure_time = flight['depDate'] + flight['depTime']  # 航班出发时间
                departure_time = departure_time.replace("-", "").replace(":", "")
                departure_time = departure_time.replace(" ", "")
                arr_time = flight['arrDate'] + flight['arrTime']  # 航班到达时间
                arr_time = arr_time.replace(" ", "")
                arr_time = arr_time.replace("-", "").replace(":", "")

            flight_seat = value['journey']['seatInfo']['nums']  # 座位信息
            cabin = value['price']['lowPriceBase']['cabin'] # 仓位信息
            flight_tax = value['price']['tax']  # 航班税
            total_price = value['price']['lowTotalPrice']  # 航班总价格
            flight_result = pares(flight_name, departure_name, departure_time, arr_name, arr_time, flight_seat, cabin, lowest_price, flight_tax, total_price, stop_cities)
            flights_data['result'].append(flight_result)
    except Exception as e:
        return {'error': f"exec_data Error,{e}"}


def pares(flightNumber, iataCode, dateTime, iataCode1, arrTime, set, cabinClass, base, taxTotal, amount, stops):
  list_flight = []
  flight_dict = {
    "flightNumber": flightNumber,
    "depAirport": iataCode,
    "depTime": ''.join(dateTime),
    "depTerminal": '',  # 登机楼
    "arrAirport": iataCode1,
    "arrTime": ''.join(arrTime),
    "arrTerminal": '',  # 登机楼
    "stopCities": stops,
    "operatingFlightNumber": '',
    "cabin": cabinClass,
    "cabinClass": "",
    "seats": set,
    "aircraftCode": "",
    "operating": 0  # 不是共享1是共享
  }
  list_flight.append(flight_dict)
  adultPrice = math.ceil(float(base))
  adultTax = math.ceil(float(taxTotal))
  adultTotalPrice = amount
  mongo_dict = {
    '_id': 'Qunargj' + '-' + str(list_flight[0]['depAirport']) + '-' + str(list_flight[-1]['arrAirport']) + '-' + str(
      list_flight[0]['depTime'])[:8] + '-' + '@'.join([str(fly_i['flightNumber']) for fly_i in list_flight]),
    'flights': [{
      'segmentsList': [list_flight],
      'currency': 'CNY',
      'adultPrice': adultPrice,
      'adultTax': adultTax,
      'adultTotalPrice': adultTotalPrice,
    }],
    'status': 0,
    'msg': '',
    'siteCode': 'Qunargj',
    'datetime': int(str(list_flight[0]['depTime'])[:8]),
    'updatetime': int(time.time()),
  }
  return mongo_dict


def depair(start_data):
    cs_june = getCs_june()
    if cs_june.get("error") is None:
        alina = get_Alina()
        if alina.get("error") is None:
            qn1 = get_QN1()
            if qn1.get("error") is None:
                cookie = f"QN1={qn1['qn1']};Alina={alina['alina']};cs_june={cs_june['cs_june']}"
                data = get_data(cookie, start_data)
                if data.get("error") is None:
                    exec_data(data.get("data"))
                else:
                    print(f"ip{start_data['proxy']}获取data出错，{data}")
                    flights_data['need'] = 1
                    flights_data['result'] = []
            else:
                print(f"ip{start_data['proxy']}获取qn1出错，{qn1}")
                flights_data['need'] = 1
                flights_data['result'] = []
        else:
            print(f"ip{start_data['proxy']}获取alina出错，{alina}")
            flights_data['need'] = 1
            flights_data['result'] = []
    else:
        print(f"ip{start_data['proxy']}获取cs_june出错，{cs_june}")
        flights_data['need'] = 1
        flights_data['result'] = []

    # print(flights_data)


if __name__ == '__main__':
    num = client.dbsize()
    threads = []
    with concurrent.futures.ThreadPoolExecutor(3) as th:
        try:
            for item in range(num):
                ip = proxy_ip()
                start_data = {
                    'from': 'SHA',
                    'to': 'SEL',
                    'daytime': '2023-08-30',
                    'adt_num': 1,
                    'chd_num': '0',
                    'inf_num': '0',
                    'fly_num': '1',
                    'limit_seat': '1',
                    'proxy': ip
                }
                future = th.submit(depair, start_data)
                threads.append(future)

            # for future in concurrent.futures.as_completed(threads):
            #     try:
            #         future.result()
            #     except Exception as e:
            #         print(f"任务执行出错{e}")
        except Exception as e:
            print(f"假数据或线程问题,{e}")