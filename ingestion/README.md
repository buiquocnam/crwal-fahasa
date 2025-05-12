# Fahasa Data Ingestion

Module này chịu trách nhiệm nhập dữ liệu sách từ file JSON (được tạo bởi Crawler) vào cơ sở dữ liệu PostgreSQL. Module này đảm bảo dữ liệu được chuẩn hóa, lọc và lưu trữ đúng cách.

## Quy trình hoạt động

### 1. Khởi tạo
- Thiết lập logging để ghi nhật ký quá trình
- Thiết lập các hằng số: đường dẫn file JSON, thông tin kết nối PostgreSQL

### 2. Đợi file dữ liệu (hàm `wait_for_data_file`)
- Kiểm tra và đợi cho đến khi file JSON từ crawler xuất hiện
- Có cơ chế chờ với số lần thử tối đa
- Đảm bảo file có nội dung và đọc được

### 3. Đọc dữ liệu từ file JSON (hàm `read_json_data`)
- Mở file JSON với encoding UTF-8 để hỗ trợ tiếng Việt
- Parse nội dung JSON thành cấu trúc dữ liệu Python
- Kiểm tra tính hợp lệ của dữ liệu
- Trả về mảng các object sách

### 4. Kết nối đến PostgreSQL (hàm `get_db_connection`)
- Thiết lập kết nối đến PostgreSQL
- Xử lý các tham số kết nối: host, port, database, user, password
- Cấu hình tự động chuyển dictionary lưới bằng DictCursor
- Có cơ chế thử lại kết nối nếu thất bại
- Trả về đối tượng kết nối để sử dụng trong các hàm khác

### 5. Tạo schema database (hàm `create_schema`)
- Tạo bảng "books" nếu chưa tồn tại
- Định nghĩa cấu trúc bảng với các trường:
  - id: SERIAL PRIMARY KEY
  - title: TEXT NOT NULL
  - author: TEXT
  - price: TEXT
  - original_price: TEXT
  - discount: TEXT
  - url: TEXT
  - image_url: TEXT
- Xử lý lỗi nếu có vấn đề khi tạo bảng

### 6. Chuẩn hóa dữ liệu (hàm `clean_book_data`)
- Nhận một object sách từ dữ liệu JSON
- Kiểm tra và đảm bảo các trường bắt buộc tồn tại
- Loại bỏ các kí tự đặc biệt không hợp lệ nếu cần
- Trả về object sách đã được chuẩn hóa

### 7. Nhập dữ liệu vào PostgreSQL (hàm `ingest_data`)
- Nhận dữ liệu sách đã được chuẩn hóa
- Kết nối đến database
- Tạo schema nếu cần
- Lặp qua từng sách và chèn vào bảng "books"
- Sử dụng transaction để đảm bảo tính toàn vẹn dữ liệu
- Đếm và ghi log số lượng sách đã được chèn thành công

### 8. Hàm chính (hàm `main`)
- Đợi file dữ liệu từ crawler
- Đọc dữ liệu JSON
- Chuẩn hóa dữ liệu sách
- Nhập dữ liệu vào PostgreSQL
- Xử lý lỗi và ghi log toàn bộ quá trình

## Điểm đặc biệt

- **Cơ chế Idempotent**: Có thể chạy nhiều lần mà không tạo ra dữ liệu trùng lặp
- **Tự động chuẩn hóa**: Đảm bảo dữ liệu sạch trước khi nhập vào database
- **Xử lý lỗi mạnh mẽ**: Có cơ chế thử lại và xử lý ngoại lệ
- **Ghi log chi tiết**: Theo dõi toàn bộ quá trình xử lý
- **Phối hợp với Crawler**: Đợi dữ liệu từ crawler trước khi xử lý

## Các tham số có thể tùy chỉnh

- `DATA_FILE`: Đường dẫn đến file JSON chứa dữ liệu sách
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Thông tin kết nối PostgreSQL
- `MAX_RETRIES`: Số lần thử lại kết nối tối đa
- `RETRY_DELAY`: Thời gian chờ giữa các lần thử lại (giây)

## Cách chạy Ingestion

1. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```

2. Đảm bảo PostgreSQL đã được khởi động và có thể kết nối

3. Chạy ingestion:
   ```
   python ingestion.py
   ```

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