# Ingestion Service

Ingestion Service là thành phần quan trọng trong kiến trúc hệ thống, chịu trách nhiệm đọc dữ liệu từ các file JSON được tạo bởi Crawler và chuyển dữ liệu này vào hệ thống cơ sở dữ liệu thông qua Database API.

## Kiến trúc

Dựa theo sơ đồ kiến trúc hệ thống, Ingestion Service có các tương tác sau:

1. **Nhận dữ liệu từ Landing Zone**: Ingestion Service đọc các file JSON được lưu trữ trong Landing Zone (được tạo bởi Crawler).

2. **Gửi dữ liệu đến Database API**: Sau khi xử lý dữ liệu từ JSON, Ingestion Service gửi dữ liệu này đến Database API để lưu trữ trong cơ sở dữ liệu.

3. **Không kết nối trực tiếp đến Database**: Ingestion Service không tương tác trực tiếp với cơ sở dữ liệu mà phải thông qua Database API.

## Quy trình hoạt động

1. **Khởi động và chuẩn bị**:
   - Đợi các dịch vụ phụ thuộc khởi động (Database API)
   - Kiểm tra kết nối đến Database API

2. **Tìm kiếm file dữ liệu**:
   - Đợi đến khi các file JSON từ Crawler sẵn sàng trong Landing Zone
   - Ưu tiên file tổng hợp nếu có, nếu không thì xử lý từng file theo danh mục

3. **Đọc và xử lý dữ liệu**:
   - Đọc dữ liệu từ các file JSON
   - Xác thực và chuẩn hóa dữ liệu nếu cần

4. **Gửi dữ liệu đến Database API**:
   - Kiểm tra xem đã có dữ liệu trong database chưa (thông qua Database API)
   - Nếu chưa có, gửi dữ liệu đến Database API để lưu trữ
   - Sử dụng phương thức phù hợp (POST/PATCH) để gửi dữ liệu

5. **Xử lý lỗi và ghi log**:
   - Ghi log toàn bộ quá trình
   - Xử lý lỗi kết nối và lỗi dữ liệu
   - Cung cấp thông tin về số lượng bản ghi đã xử lý thành công/thất bại

## Cấu hình

Ingestion Service sử dụng các biến môi trường hoặc tệp cấu hình để xác định:

- Đường dẫn đến thư mục chứa file JSON (DATA_DIR)
- Tên file tổng hợp (COMBINED_DATA_FILE)
- URL của Database API (API_BASE_URL)
- Cấu hình timeout và retry cho các yêu cầu API

## Xử lý lỗi

Ingestion Service được thiết kế để xử lý các tình huống lỗi sau:

- Database API không khả dụng
- Định dạng file JSON không hợp lệ
- Dữ liệu thiếu hoặc không đúng định dạng
- Lỗi kết nối mạng
- Lỗi xác thực hoặc phân quyền

Ingestion Service sẽ ghi log chi tiết các lỗi và cố gắng tiếp tục xử lý các bản ghi khác nếu có thể.

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