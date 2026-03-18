import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN
import shopee_api
import ranking

# Bật log để debug
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Xin chào! Tôi là Bot tìm sản phẩm Shopee rẻ và uy tín nhất. 🔍🛒\n\n"
        "Hãy gửi cho tôi:\n"
        "- **Tên sản phẩm** (VD: chuột không dây)\n"
        "- **Link sản phẩm** (để tìm loại tương đương giá tốt hơn)\n"
        "- **Ảnh sản phẩm** (sắp ra mắt)\n\n"
        "Tôi sẽ quét và trả về cho bạn 3 sản phẩm có đánh giá cao, mua nhiều và rẻ nhất!"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Kịch bản 1: Người dùng gửi Link
    url_pattern = re.compile(r'http[s]?://')
    if url_pattern.search(text) and 'shopee' in text.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="⏳ Tôi nhận thấy bạn gửi Link. Chức năng phân tích link mổ xẻ sản phẩm tương đương đang cập nhật..."
        )
        return

    # Kịch bản 2: Tìm kiếm theo Keyword (Tên sản phẩm)
    keyword = text
    processing_msg = await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"⏳ Đang tìm kiếm sản phẩm: '{keyword}' trên Shopee..."
    )
    
    # 1. Quét dữ liệu Shopee
    raw_items = shopee_api.search_products(keyword, limit=50)
    if not raw_items:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="❌ Xin lỗi, hiện tại không tìm được sản phẩm hoặc bị chặn từ API Shopee. Bạn thử đổi từ khóa khác xem sao."
        )
        return
        
    # 2. Parse dữ liệu và tính điểm
    parsed_items = [shopee_api.parse_product_info(item) for item in raw_items]
    ranked_items = ranking.rank_products(parsed_items)
    
    if not ranked_items:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="❌ Không có sản phẩm nào hợp lệ sau khi giải mã."
        )
        return
        
    # 3. Lấy ra Top 3 sản phẩm
    top_3 = ranked_items[:3]
    
    # Gửi sản phẩm TOP 1 với hình dạng "Ảnh + Tin nhắn" bắt mắt nhất
    best_item = top_3[0]
    best_price_str = f"{best_item['price']:,.0f} VND"
    caption_top1 = (
        f"🏆 **SẢN PHẨM HOÀN HẢO NHẤT** 🏆\n\n"
        f"*{best_item['name']}*\n"
        f"💰 Giá: {best_price_str}\n"
        f"⭐ Đánh giá: {best_item['rating']:.1f}/5\n"
        f"📦 Đã bán: {best_item['sold']}\n\n"
        f"🔗 Mua ngay: {best_item['link']}\n"
    )
    if best_item.get('image_url'):
        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=best_item['image_url'],
                caption=caption_top1,
                parse_mode='Markdown'
            )
        except Exception as e:
            # Fallback nếu link ảnh hỏng
            await context.bot.send_message(chat_id=update.effective_chat.id, text=caption_top1, parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=caption_top1, parse_mode='Markdown')
        
    # Gửi các tùy chọn dự phòng (TOP 2, TOP 3)
    if len(top_3) > 1:
        alt_response = f"👀 **Các lựa chọn thay thế bạn nên xem:**\n\n"
        for i, p in enumerate(top_3[1:], 2):
            price_str = f"{p['price']:,.0f} VND" if p['price'] > 0 else "Liên hệ"
            alt_response += (
                f"{i}. *{p['name']}*\n"
                f"💰 {price_str} | ⭐ {p['rating']:.1f} | 📦 Đã bán: {p['sold']}\n"
                f"🔗 {p['link']}\n\n"
            )
            
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=alt_response, 
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="📸 Tính năng tìm kiếm bằng Hình Ảnh đang được nghiên cứu tích hợp!"
    )

if __name__ == '__main__':
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️ LỖI: Không tìm thấy TELEGRAM_BOT_TOKEN. Vui lòng thêm vào file .env (nếu chạy local) hoặc cấu hình Environment trong cài đặt của Render!")
        exit(1)
        
    # Chạy một web server nền để Render không báo lỗi Timeout Port Binding
    from keep_alive import keep_alive
    keep_alive()
        
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Đăng ký các bộ xử lý
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("🚀 Bot đang chạy và lắng nghe tin nhắn...")
    application.run_polling()
