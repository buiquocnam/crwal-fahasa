# API Nhập Dữ Liệu Sách Fahasa

Dịch vụ nhập dữ liệu (data ingestion) này đọc dữ liệu sách từ các file JSON, xác thực, chuẩn hóa và nhập vào cơ sở dữ liệu thông qua API.

## Tính năng chính

- 📥 **Nhập dữ liệu tự động**: Tự động đọc và xử lý dữ liệu từ các file JSON
- ✅ **Xác thực và chuẩn hóa**: Kiểm tra và làm sạch dữ liệu trước khi nhập
- 🔄 **API Trigger**: Endpoint để kích hoạt quá trình nhập dữ liệu từ xa
- 📊 **Theo dõi trạng thái**: Endpoint để kiểm tra trạng thái nhập dữ liệu cuối cùng
- 🩺 **Health check**: Endpoint kiểm tra trạng thái hoạt động của dịch vụ
- 📝 **Ghi log**: Ghi nhật ký chi tiết toàn bộ quá trình nhập dữ liệu

## Công nghệ sử dụng

- **FastAPI**: Framework API hiệu suất cao, dễ sử dụng
- **Requests**: Thư viện HTTP cho Python để kết nối với API 
- **JSON5**: Xử lý định dạng JSON mở rộng
- **Python-dotenv**: Quản lý biến môi trường
- **PostgreSQL**: Hệ quản trị cơ sở dữ liệu (gián tiếp thông qua API)

## Cấu trúc dự án

```
data_ingestion/
├── main.py                 # Entry point ứng dụng
├── requirements.txt        # Thư viện cần thiết
├── Dockerfile              # Cấu hình Docker
├── src/
│   ├── config/             # Cấu hình
│   │   └── settings.py     # Thiết lập ứng dụng
│   ├── api/                # Tương tác với API
│   │   └── book_client.py  # Gọi API nhập sách
│   ├── validation/         # Xác thực dữ liệu
│   │   ├── schema.py       # Định nghĩa schema
│   │   └── validator.py    # Logic xác thực
│   ├── utils/              # Tiện ích
│   │   └── data_loader.py  # Đọc file JSON
│   └── ingestion.py        # Logic nhập dữ liệu chính
```

## API Endpoints

### Health Check (`GET /`)
- Kiểm tra trạng thái hoạt động của dịch vụ
- Response: `{"status": "online"}`

### Trigger Ingestion (`POST /trigger`)
- Kích hoạt quá trình nhập dữ liệu
- Response: `{"success": true}`

### Get Status (`GET /status`)
- Lấy trạng thái của lần nhập dữ liệu cuối cùng
- Response: 
  ```json
  {
    "timestamp": "2023-10-25T12:00:00.123456",
    "success": true
  }
  ```

## Quy trình nhập dữ liệu

1. **Tìm kiếm file dữ liệu**:
   - Tìm tất cả các file JSON trong thư mục dữ liệu

2. **Đọc và hợp nhất dữ liệu**:
   - Đọc từng file JSON và hợp nhất dữ liệu

3. **Xác thực và chuẩn hóa**:
   - Kiểm tra tính hợp lệ của dữ liệu theo schema
   - Chuẩn hóa dữ liệu trước khi nhập

4. **Xóa dữ liệu hiện có**:
   - Xóa tất cả sách trong cơ sở dữ liệu thông qua API

5. **Nhập dữ liệu mới**:
   - Nhập dữ liệu đã được xác thực vào cơ sở dữ liệu thông qua API batch

## Schema dữ liệu sách

```json
{
  "required": ["title"],
  "optional": [
    "price", "original_price", "discount", "author", "url", "image_url", 
    "category", "product_code", "supplier", "publisher", "publish_year", 
    "weight", "dimensions", "page_count", "cover_type", "description", "language"
  ]
}
```

Chỉ có trường `title` là bắt buộc, các trường khác là tùy chọn.

## Kết nối với API Database

Dịch vụ này kết nối với API Database (mặc định là `http://api:8000`) để thực hiện các thao tác sau:
- **Xóa tất cả sách**: `DELETE /books/deleteAll`
- **Nhập sách hàng loạt**: `POST /books/batch`
