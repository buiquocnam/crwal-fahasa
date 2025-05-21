# Dịch Vụ Thu Thập Dữ Liệu Fahasa

Dịch vụ thu thập dữ liệu (data crawling) chuyên biệt này thu thập thông tin sách từ trang web Fahasa, phân tích, và lưu trữ dữ liệu vào các file JSON để cung cấp cho hệ thống.

## Tính năng chính

- 🔍 **Thu thập dữ liệu thông minh**: Crawl sách từ website Fahasa với thông tin chi tiết
- 📊 **Đa luồng hiệu suất cao**: Mỗi danh mục được crawl trên một thread riêng biệt
- 📚 **Phân loại tự động**: Tự động phân loại sách theo danh mục
- 💾 **Lưu trữ an toàn**: Tự động sao lưu dữ liệu cũ trước khi cập nhật
- ⏱️ **Lập lịch linh hoạt**: Tự động thu thập dữ liệu theo lịch đã cấu hình
- 🔔 **Thông báo tích hợp**: Tự động thông báo cho dịch vụ ingestion khi có dữ liệu mới
- 🛡️ **Kiểm soát đầy đủ**: API quản lý để kiểm tra trạng thái và kích hoạt thủ công

## Công nghệ sử dụng

- **FastAPI**: Framework API hiệu suất cao
- **BeautifulSoup4**: Thư viện phân tích HTML/XML
- **Requests**: Thư viện HTTP cho Python
- **lxml**: Trình phân tích cú pháp HTML/XML hiệu suất cao
- **Schedule**: Lập lịch các tác vụ định kỳ
- **Concurrent.futures**: Xử lý đa luồng
- **Python-dotenv**: Quản lý biến môi trường

## Cấu trúc dự án

```
data_crawling/
├── main.py                 # Entry point ứng dụng
├── requirements.txt        # Thư viện cần thiết
├── Dockerfile              # Cấu hình Docker
├── src/
│   ├── config/             # Cấu hình 
│   │   └── settings.py     # Cài đặt và cấu hình
│   ├── crawlers/           # Logic thu thập dữ liệu
│   │   ├── crawler_runner.py  # Điều phối quá trình crawl
│   │   ├── fahasa_crawler.py  # Thu thập dữ liệu Fahasa
│   │   └── scheduler.py       # Lập lịch tự động
│   ├── parsers/            # Phân tích HTML
│   │   └── book_parser.py  # Phân tích dữ liệu sách
│   └── utils/              # Tiện ích
│       ├── file_utils.py   # Xử lý file
│       └── html_fetcher.py # Tải nội dung HTML
```

## API Endpoints

### Health Check (`GET /`)
- Kiểm tra trạng thái hoạt động của dịch vụ
- Trả về thông tin cấu hình lập lịch
- Response: 
  ```json
  {
    "status": "online",
    "scheduled_crawling": true,
    "schedule_time": "01:00"
  }
  ```

### Trigger Crawl (`POST /crawl`)
- Kích hoạt quá trình thu thập dữ liệu thủ công
- Response: `{"status": "started"}`

## Quy trình thu thập dữ liệu

1. **Khởi tạo cấu hình**:
   - Đọc cấu hình từ file JSON và biến môi trường
   - Xác định danh mục cần thu thập và thư mục đầu ra

2. **Khởi tạo đa luồng**:
   - Tạo thread riêng biệt cho mỗi danh mục
   - Thiết lập tham số cho từng thread (URL, số trang tối đa)

3. **Thu thập dữ liệu danh mục**:
   - Duyệt từng trang danh mục theo URL
   - Phân tích trang HTML để lấy danh sách sản phẩm
   - Thu thập URL của từng sản phẩm

4. **Thu thập chi tiết sách**:
   - Truy cập trang chi tiết của từng sách
   - Phân tích dữ liệu: tên, tác giả, giá, mô tả, v.v.
   - Chuẩn hóa thông tin với mapping tiếng Việt-Anh

5. **Xử lý và lưu trữ**:
   - Tạo bản sao lưu dữ liệu cũ
   - Lưu dữ liệu mới vào file JSON theo danh mục
   - Thông báo cho dịch vụ ingestion

## File cấu hình

File JSON cấu hình crawler chứa các thông tin:

```json
{
  "BASE_URL": "https://www.fahasa.com/sach-trong-nuoc",
  "ENABLED_CATEGORIES": [
    "van-hoc-trong-nuoc",
    "kinh-te",
    "tam-ly-ky-nang-song"
  ],
  "MAX_PAGES": 2,
  "OUTPUT_DIR": "/app/data",
  "SCHEDULED_CRAWLING": true,
  "SCHEDULE_TIME": "01:00"
}
```

## Dữ liệu thu thập

Mỗi cuốn sách được thu thập với các thông tin:

```json
{
  "title": "Nhà Giả Kim",
  "price": "79.000đ",
  "original_price": "100.000đ",
  "discount": "-20%",
  "image_url": "https://cdn.fahasa.com/media/catalog/product/n/h/nha-gia-kim.jpg",
  "product_code": "8935235",
  "supplier": "NXB Văn Học",
  "author": "Paulo Coelho",
  "publisher": "NXB Hội Nhà Văn",
  "publish_year": "2020",
  "weight": "220g",
  "dimensions": "13x20.5 cm",
  "page_count": "227",
  "cover_type": "Bìa mềm",
  "url": "https://www.fahasa.com/nha-gia-kim.html",
  "description": "Tiểu thuyết Nhà giả kim của Paulo Coelho...",
  "category": "van-hoc-nuoc-ngoai"
}
```

## Logging và xử lý lỗi

Dịch vụ có hệ thống ghi log đầy đủ với các mức chi tiết khác nhau:
- **INFO**: Theo dõi tiến trình thu thập dữ liệu
- **WARNING**: Cảnh báo về vấn đề không nghiêm trọng 
- **ERROR**: Lỗi xảy ra khi thu thập dữ liệu

Hệ thống cũng có khả năng phục hồi sau lỗi:
- Bỏ qua sách có lỗi và tiếp tục với sách tiếp theo
- Bỏ qua trang có lỗi và tiếp tục với trang tiếp theo
- Bỏ qua danh mục có lỗi và tiếp tục với danh mục tiếp theo

