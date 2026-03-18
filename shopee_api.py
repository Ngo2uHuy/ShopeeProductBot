import requests
import urllib.parse
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    'Referer': 'https://shopee.vn/',
}

def search_products(keyword, limit=30):
    """
    Search products on Shopee using their public Search HTTP API.
    Note: Shopee API is constantly changing.
    """
    keyword_encoded = urllib.parse.quote(keyword)
    url = f"https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={keyword_encoded}&limit={limit}&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('items', [])
        else:
            print(f"Lỗi truy xuất Shopee: {response.status_code}")
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
