# Fahasa Book API

API này cung cấp các endpoint để truy vấn dữ liệu sách từ Fahasa đã được thu thập và lưu trong cơ sở dữ liệu PostgreSQL.

## Quy trình hoạt động

### 1. Khởi tạo và cấu hình (main.py)
- Khởi tạo ứng dụng FastAPI
- Thiết lập CORS (Cross-Origin Resource Sharing)
- Đăng ký các router từ module books.py
- Tạo endpoint root (/) để kiểm tra trạng thái API
- Thiết lập event startup và shutdown để khởi tạo và đóng kết nối database

### 2. Kết nối cơ sở dữ liệu (database.py)
- Thiết lập kết nối đến PostgreSQL sử dụng psycopg2
- Định nghĩa hàm dependency `get_db()` để cung cấp connection cho các route
- Xử lý kết nối pool để tối ưu hiệu suất
- Tự động đóng kết nối khi không sử dụng

### 3. Models dữ liệu (models.py)
- Định nghĩa model Pydantic `Book` cho dữ liệu sách
- Định nghĩa model `BookList` cho danh sách sách và thông tin phân trang
- Định nghĩa model `SearchResult` cho kết quả tìm kiếm
- Cấu hình schema examples để tạo documentation

### 4. Cấu hình hệ thống (config.py)
- Định nghĩa các thiết lập cơ sở dữ liệu (host, port, username, password)
- Định nghĩa các hằng số API (giới hạn mặc định, giới hạn tối đa)
- Thiết lập logging

### 5. API Endpoints (books.py)

#### 5.1 Lấy danh sách sách (`GET /books/`)
- Nhận tham số: limit, offset, title (tùy chọn)
- Tham số limit quy định số lượng sách trả về
- Tham số offset dùng cho phân trang
- Tham số title dùng để lọc theo tiêu đề
- Truy vấn database và trả về danh sách sách theo các tiêu chí

#### 5.2 Lấy chi tiết một cuốn sách (`GET /books/{book_id}`)
- Nhận tham số path: book_id
- Truy vấn database với ID cụ thể
- Trả về thông tin đầy đủ của sách hoặc 404 nếu không tìm thấy

#### 5.3 Tìm kiếm sách theo tiêu đề (`GET /books/search/title`)
- Nhận tham số: keyword, limit, offset
- Truy vấn database với điều kiện ILIKE %keyword% trên cột title
- Trả về kết quả tìm kiếm và thông tin phân trang

#### 5.4 Tìm kiếm sách theo tác giả (`GET /books/search/author`)
- Nhận tham số: keyword, limit, offset
- Truy vấn database với điều kiện ILIKE %keyword% trên cột author
- Trả về kết quả tìm kiếm và thông tin phân trang

## Đặc điểm kỹ thuật

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Xử lý JSON**: Pydantic
- **CORS**: Hỗ trợ cross-origin requests
- **Phân trang**: Hỗ trợ thông qua tham số limit và offset
- **Tìm kiếm**: Hỗ trợ tìm kiếm theo tiêu đề hoặc tác giả
- **Logging**: Ghi log chi tiết quá trình xử lý

## Cấu trúc response

### Danh sách sách và kết quả tìm kiếm
```json
{
  "total": 120,
  "limit": 10,
  "offset": 0,
  "books": [
    {
      "id": 1,
      "title": "Nhà Giả Kim",
      "price": "79.000đ",
      "original_price": "100.000đ",
      "discount": "-20%",
      "author": "Paulo Coelho",
      "url": "https://www.fahasa.com/nha-gia-kim.html",
      "image_url": "https://cdn1.fahasa.com/media/catalog/product/image_195509_1_36793.jpg"
    },
    // ...các sách khác
  ]
}
```

### Chi tiết sách
```json
{
  "id": 1,
  "title": "Nhà Giả Kim",
  "price": "79.000đ",
  "original_price": "100.000đ",
  "discount": "-20%",
  "author": "Paulo Coelho",
  "url": "https://www.fahasa.com/nha-gia-kim.html",
  "image_url": "https://cdn1.fahasa.com/media/catalog/product/image_195509_1_36793.jpg"
}
```

## Cách chạy API

1. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```

2. Chạy API:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. Truy cập documentation tại:
   ```
   http://localhost:8000/docs
   ```

## Cách chạy trong Docker

1. Xây dựng image Docker:
   ```
   docker build -t fahasa-api -f Dockerfile.api .
   ```

2. Chạy container:
   ```
   docker run -p 8000:8000 fahasa-api
   ```

## Endpoint Examples

1. Lấy 10 sách đầu tiên:
   ```
   GET /books/?limit=10&offset=0
   ```

2. Lấy chi tiết sách có ID=1:
   ```
   GET /books/1
   ```

3. Tìm kiếm sách có tiêu đề chứa từ "kim":
   ```
   GET /books/search/title?keyword=kim&limit=10&offset=0
   ```

4. Tìm kiếm sách của tác giả có tên chứa "nguyen":
   ```
   GET /books/search/author?keyword=nguyen&limit=10&offset=0
   ```

## Cấu trúc dự án

```
api/
├── config.py        # Cấu hình, hằng số
├── database.py      # Kết nối và xử lý database
├── main.py          # Entry point của ứng dụng FastAPI
├── models.py        # Pydantic models 
├── books.py         # Router và xử lý endpoint sách
└── README.md        # Tài liệu dự án
```

## Khởi động API

Để chạy API, sử dụng lệnh sau từ thư mục api/:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /books`: Lấy danh sách sách với phân trang
- `GET /books/{book_id}`: Lấy thông tin sách theo ID
- `GET /books/search/title`: Tìm kiếm sách theo tiêu đề
- `GET /books/search/author`: Tìm kiếm sách theo tác giả 