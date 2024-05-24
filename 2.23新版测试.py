import requests


headers = {
    "authority": "flight.qunar.com",
    "accept": "text/javascript, text/html, application/xml, text/xml, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "app": "0%2C0%2C%2C2",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded",
    "csht": "",
    "pragma": "no-cache",
    "pre": "650a89cb-80e373-764f8770-26a15001-608d49959f2e",
    "referer": "https://flight.qunar.com/site/oneway_list_inter.htm?searchDepartureAirport=%E5%8C%97%E4%BA%AC&searchArrivalAirport=%E9%A6%96%E5%B0%94&searchDepartureTime=2023-08-30&searchArrivalTime=2023-09-14&nextNDays=0&startSearch=true&fromCode=BJS&toCode=SEL&from=qunarindex&lowestPrice=null&favoriteKey=&showTotalPr=null&adultNum=1&childNum=0&cabinClass=",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "QN1": "000063002e1854e06a98e4cf",
    "QN601": "244b0a25d2e664aed268bc66a7dd10f2",
    "QN300": "flight.qunar.com",
    "QN99": "759",
    "SplitEnv": "D",
    "ctt_june": "1683616182042##iK3waSPnWwPwawPwa%3DfTWsXAWS38XSjsWSHTWSa8aRXOWKkhWR3NERGRX2XniK3siK3saKjNaSgOas2mVKt%2BWwPwaUvt",
    "ctf_june": "1683616182042##iK3wWRasVuPwawPwa%3DanaSGGW2XAEDETVRWIaDETVRWIXPPAa2Gha%3DaNX%3DfDiK3siK3saKjNaSgOas2mVKtNaUPwaUvt",
    "qunar-assist": "{%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}",
    "QN48": "8936e88e-3732-44cc-adac-8ec7a6013ab0",
    "F234": "1692763990299",
    "F235": "1692763990299",
    "cs_june": "cdc0d3cfef4ecef746275d9f8525b42e3f091e11c8b3b08eb4dbf911f3f3afc3f0136b869b75cde56790c74406825ebabc84c5f6a97ffc352d546fbefd1516e7b17c80df7eee7c02a9c1a6a5b97c1179c77c14abc4ae3715e6b31348e251ddf15a737ae180251ef5be23400b098dd8ca",
    "QN267": "068612685185bc8cef",
    "csrfToken": "RzUp4uyb6yUfkiF7QFNTwA1X94D7MQVB",
    "_i": "ueHd8LkXXXVXrXNy-TASOW46DZYX",
    "_vi": "2JuH6kCPZH230kxQrI1U4-DxqdiMfqacAmz8cWP1AKfaM6BrHQ10u8VNfVrQTdyFZCeCd4M4snyAV92wa02gVIW1aUuRrjLScYzlbqXtGMB7mqVV4au7J6N_uhZq_4jcwIcVFVysygtyeSnYy2IWuwDN3V_jUK4aVfKd0hBZBYHj",
    "QN621": "fr%3Dqunarindex",
    "Alina": "99eadd93-812c58-794a8261-37905973-12cc64e58756",
    "QN269": "5EE16540416B11EEA97FFA163E0BBFA6",
    "quinn": "e3b6a663ae578e247eb28eb7aded0d74d9352520122971229f36e96b1bad57381bbc79d9b2bfa02621383c1d06ed67ce",
    "fid": "69a50225-da52-49c5-9773-2acdb0b636fd",
    "QN271": "1ac24374-0243-4c56-9ab7-4a0bb092896d",
    "QunarGlobal": "10.72.85.166_43b38895_18a1ed84390_-5171%7C1692763993276"
}
url = "https://flight.qunar.com/touch/api/inter/wwwsearch"
params = {
    "depCity": "北京",
    "arrCity": "首尔",
    "depDate": "2023-08-30",
    "adultNum": "1",
    "childNum": "0",
    "ex_track": "",
    "from": "qunarindex",
    "carrier": "",
    "queryId": "10.72.85.166:l:43b38895:18a1ed84390:-5172",
    "es": "",
    "_v": "8",
    "st": "1692763990411",
    "Bella": "1683616182042##d6b786fd50767612ab9690b1e2677bf1d2171c90##iKohiK3wgMkMf-i0gUPwaUPsXuPwaMfLy9opohNno9NHgUNScO=0a2fsy-X0aS30a2a0aSi8y9WScOnxiK3wiKWTiK3wVRDNWuPwawPwa=asVDa8XPihXSTIWsa+WRD0aSa0aSanWS2wWsjsVK2mWKv=iK3wiKiRiK3wgOHQgMn0duPwaUPsXuPwa5kbyONxoOm0aS30a2a0aSi=y-ELfuPwaUPsXuPwaUkGWwkhEhPNakGAcMGwqMWxcuPwaUPwXwPwaMe0d-oxgMEsiK3wiKWTiK3wiKiRP-kbj-3bjOFeiK3wiKiRiK3wfIksj+iQgCEQcOm0aS30a=D0aS30EKP0VDP0X230EKP0VKa0XPD0EKP0VRX0X2jpP-kbj-3bjOFeJukGWhkhEhPNXwkGWhkhVhkhXukGWuPmWukTVhkGWwPNahPmawkGWUPNXwPmahkGWukTWhkTWwPwaUPwXwPwaMHxg+X0aS30a=D0aSiMcI05yCXbg-kbj-3bjOFeiK3wiKiRiK3wgOWwy-T=P+iSiK3wiKWTiKkhiK3wcCvbfMnQfOH=q5GAcMGwqUPwaUPwXwPwa5iej+W2fUNno9NHgUNScO=0aS30WPX0a2a0aSisy9obiK3wiKWTiK3wfRfUWstOfMXAaRgOWsjnaMGUVKjNaI3nfK3OWsoUfSG2aSD+a9aNahPwaUPwXwPwa5iHcMExcPNAcuPwaUPsXuPwa5oOdIiTa+HTy2eTVDF-WSPAa5iUWUPwaUPwXwPwa5X0aS30a=DnWS2wWsjsVK2mWKvAiKoD##wvxbA3xAjKA8OW6552rb6##depCity,arrCity,depDate,adultNum,childNum,ex_track,from,carrier,queryId,es,_v,st"
}
response = requests.get(url, headers=headers, cookies=cookies, params=params)

print(response.text)
print(response)