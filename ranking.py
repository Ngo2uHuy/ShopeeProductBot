def rank_products(products_list):
    """
    Xếp hạng sản phẩm dựa trên 3 tiêu chí:
    - Giá (càng rẻ càng tốt)
    - Đã bán (càng nhiều càng tốt)
    - Rating (càng cao càng tốt)
    """
    if not products_list:
        return []
        
    valid_items = [p for p in products_list if p is not None]
    if not valid_items:
        return []

    # Tìm max để chuẩn hóa Min-Max Scaling (đưa về thang 0..1 để dễ chấm điểm)
    max_price = max((p['price'] for p in valid_items if p['price'] > 0), default=1)
    max_sold = max((p['sold'] for p in valid_items if p['sold'] > 0), default=1)
    
    ranked_items = []
    for p in valid_items:
        # Chuẩn hóa
        norm_rating = p['rating'] / 5.0
        norm_sold = min(p['sold'] / max_sold, 1.0) if max_sold > 0 else 0
        norm_price = min(p['price'] / max_price, 1.0) if max_price > 0 else 1
        
        # Trọng số có thể điều chỉnh để tìm sản phẩm 'tốt nhất'
        weight_rating = 0.4  # Ưu tiên chất lượng (sao) cao
        weight_sold = 0.3    # Ưu tiên shop bán được nhiều hàng
        weight_price = 0.3   # Ưu tiên giá rẻ (trừ đi vì giá rẻ thì norm_price phải nhỏ)
        
        score = (norm_rating * weight_rating) + (norm_sold * weight_sold) - (norm_price * weight_price)
        p['score'] = score
        ranked_items.append(p)
        
    # Sắp xếp thẹo score từ cao xuống thấp
    ranked_items.sort(key=lambda x: x['score'], reverse=True)
    return ranked_items
