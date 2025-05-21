# Dịch vụ Thu thập Dữ liệu Sách
Dịch vụ này thu thập dữ liệu sách từ trang web bán sách trực tuyến Fahasa. 

## Tính năng chính

- **Thu thập dữ liệu Fahasa**: Chuyên biệt thu thập dữ liệu sách từ trang web Fahasa
- **Phân loại dữ liệu**: Tự động phân loại sách theo danh mục
- **Đa luồng xử lý**: Mỗi danh mục được crawl trong một thread riêng biệt
- **Lưu trữ dữ liệu**: Lưu trữ dữ liệu vào các file JSON theo danh mục
- **Sao lưu tự động**: Tự động tạo bản sao lưu khi cập nhật dữ liệu
- **API điều khiển**: API đơn giản để kiểm tra trạng thái và kích hoạt thu thập dữ liệu
- **Lịch trình**: Hỗ trợ thu thập dữ liệu theo lịch định sẵn

## Cấu trúc dự án

```
data_crawling/
├── main.py              # Điểm khởi đầu ứng dụng
├── requirements.txt     # Thư viện phụ thuộc
├── .env                 # Cấu hình môi trường
└── src/
    ├── config/          # Cấu hình ứng dụng
    ├── crawlers/        # Mã nguồn thu thập dữ liệu
    │   ├── crawler_runner.py    # Điều phối quá trình crawl
    │   ├── fahasa_crawler.py    # Thu thập dữ liệu từ Fahasa
    │   └── scheduler.py         # Lập lịch crawl tự động
    ├── parsers/         # Phân tích cú pháp HTML 
    └── utils/           # Tiện ích và công cụ hỗ trợ
```

## Cách hoạt động

### Quy trình thu thập dữ liệu

1. **Khởi tạo**: Đọc cấu hình từ file `.env` (danh mục cần crawl, số trang tối đa, v.v.)
2. **Tạo thread**: Khởi tạo thread riêng biệt cho mỗi danh mục sách cần thu thập
3. **Thu thập dữ liệu**: Mỗi thread thực hiện:
   - Gửi request đến trang web
   - Phân tích HTML để lấy thông tin sách trong danh sách
   - Thu thập thông tin chi tiết của từng cuốn sách
   - Lưu trữ thông tin vào bộ nhớ tạm
4. **Xử lý kết quả**: Khi các thread hoàn thành:
   - Tạo bản sao lưu cho dữ liệu hiện có (nếu có)
   - Lưu dữ liệu mới vào file JSON theo danh mục
   - Thông báo cho dịch vụ ingestion

### API

API đơn giản cung cấp các endpoint:

- **GET /** - Kiểm tra trạng thái API và cấu hình lịch crawl
- **POST /crawl** - Kích hoạt quá trình crawl thủ công

## Cấu hình

Dịch vụ sử dụng file `.env` để cấu hình các tham số:

- `BASE_URL`: URL cơ sở của trang web cần crawl
- `ENABLED_CATEGORIES`: Danh sách các danh mục cần crawl
- `MAX_PAGES`: Số trang tối đa crawl cho mỗi danh mục
- `SCHEDULED_CRAWLING`: Bật/tắt chế độ crawl theo lịch
- `SCHEDULE_TIME`: Thời gian crawl theo lịch (định dạng HH:MM)
- `INGESTION_CALLBACK_URL`: URL callback cho dịch vụ ingestion

## Xử lý lỗi

Dịch vụ có hệ thống logging đầy đủ:

- Logs được lưu với các mức độ khác nhau (DEBUG, INFO, WARNING, ERROR)
- Mỗi crawler có xử lý ngoại lệ riêng
- Quá trình crawl vẫn tiếp tục ngay cả khi một danh mục gặp lỗi
- Backup dữ liệu trước khi ghi đè
