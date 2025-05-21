# API Sách Fahasa

API RESTful cung cấp các endpoint để quản lý và truy vấn dữ liệu sách từ Fahasa được lưu trữ trong cơ sở dữ liệu PostgreSQL.

## Tính năng chính

- 📚 **Quản lý sách**: Tìm kiếm, lấy chi tiết, thêm mới và xóa sách
- 🔍 **Tìm kiếm đa dạng**: Tìm kiếm sách theo tiêu đề, tác giả, hoặc thể loại
- 📊 **Phân trang**: Hỗ trợ phân trang kết quả với tham số limit và page
- 🔄 **CORS**: Hỗ trợ Cross-Origin Resource Sharing
- 🩺 **Health check**: Endpoint kiểm tra trạng thái hoạt động
- 📝 **OpenAPI**: Tài liệu API tự động sinh với Swagger UI

## Công nghệ sử dụng

- **[FastAPI]**: Framework API hiệu suất cao, dễ sử dụng
- **[SQLAlchemy]**: ORM mạnh mẽ để tương tác với PostgreSQL
- **[Pydantic]**: Kiểm tra kiểu dữ liệu và kiểm soát lỗi
- **[PostgreSQL]**: Hệ quản trị cơ sở dữ liệu quan hệ
- **[Docker]**: Container hóa ứng dụng

## Cài đặt và Chạy

### Sử dụng môi trường ảo Python

1. Tạo môi trường ảo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

3. Cấu hình biến môi trường trong file `.env`:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=fahasa_db
   DB_USER=your_user
   DB_PASS=your_password
   ```

4. Chạy ứng dụng:
   ```bash
   uvicorn database_api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Cấu trúc dự án

```
database_api/
├── main.py                 # Entry point ứng dụng
├── requirements.txt        # Thư viện cần thiết
├── Dockerfile              # Cấu hình Docker
├── src/
│   ├── config/             # Cấu hình
│   │   └── settings.py     # Thiết lập ứng dụng
│   ├── database/           # Xử lý cơ sở dữ liệu
│   │   └── init_db.py      # Khởi tạo và kết nối DB
│   ├── models/             # Định nghĩa model
│   │   └── book.py         # Model Sách (SQLAlchemy & Pydantic)
│   ├── repositories/       # Xử lý truy vấn dữ liệu  
│   │   └── book_repository.py  # Repository pattern cho sách
│   ├── routers/            # API endpoints
│   │   └── book_router.py  # Router sách
│   └── services/           # Logic nghiệp vụ
│       └── book_service.py # Dịch vụ sách
```

## API Endpoints

### Sách (`/books`)

- `GET /books/`: Lấy danh sách sách với phân trang và lọc
  - Query parameters:
    - `limit`: Số lượng bản ghi tối đa trả về (mặc định: 10)
    - `page`: Số trang hiện tại (mặc định: 1)
    - `title`: Lọc theo tiêu đề (tùy chọn)
    - `author`: Lọc theo tác giả (tùy chọn)
    - `category`: Lọc theo thể loại (tùy chọn)

- `GET /books/{book_id}`: Lấy thông tin sách theo ID

- `POST /books/batch`: Tạo nhiều sách cùng lúc
  - Body: Danh sách dữ liệu sách

- `DELETE /books/deleteAll`: Xóa tất cả sách

- `GET /books/categories/list`: Lấy danh sách tất cả các danh mục sách

