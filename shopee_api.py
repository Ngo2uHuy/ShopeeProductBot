import requests
import urllib.parse
import json
from config import SHOPEE_COOKIE

# Các Headers sao chép chính xác từ trình duyệt (Bao gồm token DataDome, x-sap, sz-token...)
HEADERS = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9,ja;q=0.8,vi;q=0.7",
    "af-ac-enc-dat": "4ad0eb2ac9338dc6",
    "af-ac-enc-sz-token": "tscxVHOwE0MEXaUt33r34A==|S4kLyM2sBreTtvuUAkVaxrBAdaT+WeJ7t6GQxnwbwZ3bwpxI9CnG+/CGNA5oeTYHWXXE+D1ViJ6Hpw==|1G7CeeIQmPm03PBx|08|3",
    "content-type": "application/json",
    "cookie": "_gcl_au=1.1.1602702535.1773628502; _med=refer; _QPWSDCXHZQA=110ce0e0-e7ed-4f80-ba1b-5ca89fcba43d; REC7iLP4Q=a5adb7a4-94e3-40b9-a90e-73de52ba143b; SPC_F=VdNWcFJUbeY9z2sfwtAsx7QhwNV2nDFy; REC_T_ID=bcadb993-20e0-11f1-9d6a-3abf9306c8f7; SPC_CLIENTID=VmROV2NGSlViZVk5abwzgupfpkeaohje; language=vi; _hjSessionUser_868286=eyJpZCI6IjY0ZGI1OWE1LWY5YjMtNWNjNi1iZGU5LTBjYjZkYTdhY2U1NiIsImNyZWF0ZWQiOjE3NzM2Mjg1MDQ1MTIsImV4aXN0aW5nIjp0cnVlfQ==; _ga_4GPP1ZXG63=deleted; csrftoken=8Xg7fPRiefS6ooxkR4RjH6g8sARxvWgS; _sapid=974f816dc123360492124d6fa5d4aee3c625cf550d0674a42510240b; SPC_IA=1; SPC_SI=V9C3aQAAAABiUWhsMnQ1cv+nSAAAAAAATUcwRTdMbmY=; SPC_SEC_SI=v1-bnFvSFhxZ2FuZE9QWFlUVWnjAUsRr47S12Qq1oNAVVsO6O6o8Wr7dYxVPASDXR84ErwamM2GutmiOhFvQCGiuraNIN1AKZnRqt651EyWioc=; _ga=GA1.1.2091875921.1773628504; _hjSession_868286=eyJpZCI6IjgxNWZmOTZmLTFmMTAtNDViOS04ZDIwLWJjMWMxZWNiODY1NCIsImMiOjE3NzM4NTM0MDgxMzEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; SPC_CDS_CHAT=3fb805ca-a231-4826-b21d-30d7e304b1f3; SPC_ST=WXJhT1AyNG5QR21HTUdDMzQqQlxC83NP8xGBL5pXUzeaPRiAuivEMqEfM6zsxYAjCUevt2BiueuQWdYDigLPt35ri5l3x4jk+bfwfc4V4ilGZF1Si4v7d8cQOUyLh2pubqNjzpDkPeB33Q9dTprKuI+fPNi1Hmie5QFMecQ7XH4uRfWNNuwEOrcG3g1hvB0NcjTu5m00OWeyZM0FLtITtiBcqJgtGVTfMcqiKFHjr1SvsS2jx+ZV58NTdds2emoS.AH08h5cNv9bENNT8WC8Bz2wLh5pyuSfQuXuXRQJQbkAY; SPC_U=1674148928; SPC_T_ID=UzuRQ0+z20SgTp5HGQmeDAfSJh+qnpSLY29Sq62jIq3iXnjk+J0JbCAks53VEspi9SQ1rOqmLbpcDG6PQDJBarRmNSwTh6cMKqCped0OdzBUsI1I+KQC4FrDAzcz+BK6sA0RnL4O4stm/5fHOjAZg2NMQqQiDQjC+rZuzbWa79s=; SPC_T_IV=NHUxcDdIMlF2VmMwMUUxYw==; SPC_R_T_ID=UzuRQ0+z20SgTp5HGQmeDAfSJh+qnpSLY29Sq62jIq3iXnjk+J0JbCAks53VEspi9SQ1rOqmLbpcDG6PQDJBarRmNSwTh6cMKqCped0OdzBUsI1I+KQC4FrDAzcz+BK6sA0RnL4O4stm/5fHOjAZg2NMQqQiDQjC+rZuzbWa79s=; SPC_R_T_IV=NHUxcDdIMlF2VmMwMUUxYw==; AC_CERT_D=gqRjZGVrxHeFomtpuDE0MjUxOmNhcHRjaGFfY29va2llX2tleaJrdtEAAaRhbGdv0gAAAGSjZGVrwKJjdMRAAAAADLYAun++BIGckVmcUtMeG2di+9duyfpYoiepKSRU8OsBQcF04ag1osmHaNk6MFpFrrlQbaYW2syWyKVpS6pjaXBoZXJ0ZXh0xQNLAAAADM6KbNRuYtruqbOt1geU8NvrkzDXvCfwDDY8iNH4CvZrH+uCttjP4YzLgPxdEXyHVnasAipQrOUKfm+MD6FAHzbGapOuQz8Z0Kyd0NDVMXR9z926QW193I7OudRrYgNGjL0Q9EHGrFtrjptjFogQ2/HxHBJJkm8ef8nXYb77H8PXVFFQL6fV+kRKQVcMMzjY1E8NdMRqXzeARtIdsNKz9b7ib8EYt3Eg5pHQH3BAZDzwU6GYxG0ILyvfRbys8OOIiGdLoXcSCnpI5onxe+jCyuezIwwbACJuVWdueNKpZM9t2p8IIrOz6JYbXow5ihz3lJImgfgyy6mRMz5uS14TAcGbkOFe5IQbJKgLxeoxkmiTqVRadtE2r0sMb1IYb9PGHkDGGRQNnEHVtBKay8d1ITLr1MWgor9vmPkpRN/Mj8RMXuassUkBmea2MD+k6CYnXpklOF0fAoweHVLqCSqNu5kU0byGYyWfGg6tYugJNm2ajk3xDud+mrxF/sOquLGK0prHeRg8fifdIz1bJPEgRtCPB3bRjXSQOU36SudwdgyK5+uEi9NFdZW0pkqRLmEHCrtqSpHnxGNXjpMmUM0d60xwOwd4EDoV8L8VAghP4mLEcwSFMZoiL+zheegi8C4QsCHS12CEVgUbGw7oF5NFgA1n19V9kb7iHuGqdPeO+Ez6yUXO2xo5Z9ZvpOFOzykHVva0e//lfegb6ptd194n/mLMPnaqMJQUHB4+w2WhB3q44yxuqtFeXgdPoyUP4A6PCju9U3ER2yv/S7h1AWG5vzfz/ZkEcLyFPRTrpb2G7jUkBD23H3O1eKuAlOLEKlVefNs2SMpAe0+DzNjs6JwJCzaWXjtNUcUlEcavzTD3Lg7imgScj4RhBRzw9aw5l5BTdyefXoxXk3x1vTuGHVVgjmVptnp6/AgumKtFAYLA2oPDhfwvu9POAOiCOR5L17IP1CGBGpmuLCJ3bmrtVgY/ZSPJVSTN1VKshYtBYrfA9sE0ioGeeS3cy2+YeSoGR0SrdQi2LM6HUhJ6igmXdXOssGu9+aOzMs3zI5hIOZ2lC4Q0oRJuZxcxvTYbi6Wmq03FxI/4z37imZx3DhnRNU0p8zfmVFu9v6ts; shopee_webUnique_ccd=cFXSyCj+1g6US+lvj3VJ1w==|SIkLyM2sBreTtvuUAkVaxrBAdaT+WeJ7t6GQxhMxwZ3bwpxI9CnG+/CGNA5oeTYHWXXE+D1ViJ6Hpw==|1G7CeeIQmPm03PBx|08|3; ds=e3dbfd1bdce76239587f5575626fcf16; _ga_4GPP1ZXG63=GS2.1.s1773853407$o4$g1$t1773853765$j34$l1$h1531738056; SPC_EC=Y1oyYUFPT3JuWGhMTUowMnAWMQhL3tapvPFjrmi7onH1n4qC1GnDzgDxiqVPmROXWSf7wY+wQlXiZnLJYRWhrLbW9UanWcVi271P+MF4+JPAXPc2PkIhdp862CZ98yliK3JO8hlOfMKGjPLd6jHZNmjuneQfQEZQ627vKUyDSg/nd8Lk/C1MJvc2oOVJxz0dXTwnyGKExKpfK3irD8V5bZ6VmGevTLw6lcGyZYAFo1Ypa2ujAzKmtRQk+dq8xfcX.AFO4JpdzwZrZMIzJjmqC/u7lYNcz5n25xmf5CkD20ZEM",
    "d-nonptcha-sync": "AAAG7TLjPhMBFAAzODIxODc5MjI1ZTg0YzlmYTZlMDE0MTJjOWQwNDM0MAAAX8sKGOaTMptr9wQAADMXAHNlYXJjA|7|B/wA|21|EAAAzGABzZWFyYwA|7|f8A|21|BAAAMxkAc2VhcmMA|7|H/A|22|QAADMaAHByZV9zcG9wdWwJ/wA|21|EAAAzGgBzZWFyYwA|7|f8A|21|BAAAMxsAc2VhcmMA|7|H/A|22|QAADMbAHNlYXJjA|7|B/wA|21|EAAAzHABzZWFyYwA|7|f8A|21|BAAAMx0Ac2VhcmMA|7|H/A|22|QAADMdAHNlYXJjA|7|B/wA|21|EAAAzHgBzZWFyYwA|7|f8A|21|BAAANLUAc2VhcmMA|7|L/A|15|BHRfZfwQAADS2AHNlYXJjA|7|C/wA|15|R0X2X8EAAA0tgBzZWFyYwA|6|Cf8A|21|BAAANuoAc2VhcmMA|7|H/A|22|QAADbqAHNlYXJjA|7|B/wA|21|EAABVqgBwcmVfc3NlYXJjCf8A|21|BAAAVawAcHJlX3NzZWFyYwn/A|22|QAAFWtAHByZV9zc2VhcmMJ/wA|21|EAABVrgBwcmVfc3NlYXJjCf8A|21|UHMAAChTUHMAACjvUHMAACkdRXIAACvtRXIAAFCI",
    "priority": "u=1, i",
    "referer": "https://shopee.vn/",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sz-token": "tscxVHOwE0MEXaUt33r34A==|S4kLyM2sBreTtvuUAkVaxrBAdaT+WeJ7t6GQxnwbwZ3bwpxI9CnG+/CGNA5oeTYHWXXE+D1ViJ6Hpw==|1G7CeeIQmPm03PBx|08|3",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-api-source": "pc",
    "x-csrftoken": "8Xg7fPRiefS6ooxkR4RjH6g8sARxvWgS",
    "x-requested-with": "XMLHttpRequest",
    "x-sap-ri": "51dcba69ee8dd18e0fd01a380901f18b801f32b1d04de068e1e7",
    "x-sap-sec": "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",
    "x-shopee-language": "vi",
    "x-sz-sdk-version": "1.12.33"
}


def search_products(keyword, limit=30):
    """
    Search products on Shopee using their public Search HTTP API.
    Note: Shopee API is constantly changing and aggressively blocks bots.
    """
    keyword_encoded = urllib.parse.quote(keyword)
    url = f"https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={keyword_encoded}&limit={limit}&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('items', [])
        else:
            print(f"Lỗi truy xuất Shopee: Mã lỗi {response.status_code}")
            if response.status_code == 403:
                print("==> Bị chặn bởi hệ thống bảo mật của Shopee (DataDome/Anti-bot). Cần cung cấp SHOPEE_COOKIE!")
            return []
    except Exception as e:
        print(f"Exception during search: {e}")
        return []

def parse_product_info(item_data):
    """
    Extract key product info from Shopee's item dictionary.
    """
    try:
        # Tùy phiên bản API, data sản phẩm nằm trong item_basic hoặc trực tiếp trên item
        basic = item_data.get('item_basic', item_data)
        
        name = basic.get('name', '')
        # Giá Shopee thường nhân 100,000 (vd: 120000000 -> 1,200,000)
        price = basic.get('price', 0) / 100000 
        historical_sold = basic.get('historical_sold', 0)
        
        rating_info = basic.get('item_rating', {})
        rating = 0.0
        if isinstance(rating_info, dict):
            rating = rating_info.get('rating_star', 0.0)
            
        item_id = basic.get('itemid', '')
        shop_id = basic.get('shopid', '')
        
        # Link chuẩn của Shopee
        link = f"https://shopee.vn/product/{shop_id}/{item_id}"
        
        return {
            "name": name,
            "price": price,
            "sold": historical_sold,
            "rating": rating,
            "link": link
        }
    except Exception as e:
        print(f"Error parsing item: {e}")
        return None
