# Fahasa Ingestion Service

Dịch vụ này nhận dữ liệu được crawl từ website Fahasa và nhập vào cơ sở dữ liệu PostgreSQL thông qua API.

## Cấu trúc mã nguồn

```
ingestion/
├── __init__.py             # Package initialization
├── config/                 # Cấu hình và thiết lập
│   ├── __init__.py
│   └── settings.py         # Các hằng số và cấu hình
├── validation/             # Logic kiểm tra dữ liệu
│   ├── __init__.py
│   ├── schema.py           # Định nghĩa schema dữ liệu
│   └── validator.py        # Hàm xác thực và chuẩn hóa dữ liệu
├── utils/                  # Tiện ích hỗ trợ
│   ├── __init__.py
│   ├── api_client.py       # Tương tác với API
│   └── data_loader.py      # Tải dữ liệu từ file JSON
└── main.py                 # Điểm vào chính của ứng dụng
```

## Quy trình làm việc

1. Dịch vụ khởi động và đợi các file dữ liệu từ crawler
2. Đọc dữ liệu từ file JSON (ưu tiên file tổng hợp)
3. Xác thực và chuẩn hóa dữ liệu
4. Gửi dữ liệu tới API để lưu vào cơ sở dữ liệu

## Các Module

### Config

- **settings.py**: Chứa các cấu hình hệ thống như đường dẫn, URL, biểu thức chính quy, và thiết lập logger.

### Validation

- **schema.py**: Định nghĩa cấu trúc dữ liệu sách (trường bắt buộc, tùy chọn, kiểu dữ liệu) và ánh xạ giữa các trường.
- **validator.py**: Cung cấp các hàm để kiểm tra tính hợp lệ và làm sạch dữ liệu sách.

### Utils

- **data_loader.py**: Xử lý việc đọc dữ liệu từ file JSON và quản lý các file dữ liệu.
- **api_client.py**: Xử lý giao tiếp với API, hỗ trợ nhập dữ liệu theo lô hoặc từng cuốn.

### Main

- **main.py**: Điều phối toàn bộ quy trình ingestion, từ việc đợi dữ liệu, đọc file, và xử lý đến khi nhập vào database.

## Xử lý lỗi

Hệ thống có một cơ chế xử lý lỗi mạnh mẽ với nhiều cấp độ:

1. Xử lý lỗi khi đọc file JSON
2. Xác thực và loại bỏ dữ liệu không hợp lệ
3. Thử sử dụng API batch trước (hiệu suất cao)
4. Chuyển sang nhập từng cuốn nếu batch thất bại
5. Ghi log chi tiết ở mỗi bước

## Cách chạy trong Docker

1. Xây dựng image Docker:
   ```
   docker build -t fahasa-ingestion -f Dockerfile.ingestion .
   ```

2. Chạy container:
   ```
   docker run fahasa-ingestion
   ```

## Output mẫu

```
2025-05-12 10:14:10,398 - INFO - Đang đợi file dữ liệu /app/data/fahasa_data.json...
2025-05-12 10:14:10,398 - INFO - Đã tìm thấy file dữ liệu
2025-05-12 10:14:10,399 - INFO - Đang đọc dữ liệu từ file JSON...
2025-05-12 10:14:10,401 - INFO - Đọc thành công 120 sách từ file JSON
2025-05-12 10:14:10,401 - INFO - Đang kết nối tới PostgreSQL...
2025-05-12 10:14:10,404 - INFO - Kết nối thành công
2025-05-12 10:14:10,404 - INFO - Đang tạo schema database...
2025-05-12 10:14:10,406 - INFO - Schema đã được tạo hoặc đã tồn tại
2025-05-12 10:14:10,406 - INFO - Đang nhập dữ liệu vào PostgreSQL...
2025-05-12 10:14:10,450 - INFO - Đã nhập thành công 120 sách vào database
2025-05-12 10:14:10,450 - INFO - Quá trình nhập dữ liệu hoàn tất
``` 