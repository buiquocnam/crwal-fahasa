# Fahasa Book API

API này cung cấp các endpoint để truy vấn dữ liệu sách từ Fahasa đã được thu thập và lưu trong cơ sở dữ liệu PostgreSQL.

## Quy trình hoạt động

### 1. Khởi tạo và cấu hình (main.py)
- Tạo và cấu hình ứng dụng FastAPI
- Thiết lập middleware, exception handlers và app events
- Đăng ký các router
- Tạo endpoint root (/) để kiểm tra trạng thái API

### 2. Cấu trúc mô-đun
- **config**: Quản lý cấu hình hệ thống và biến môi trường
- **core**: Xử lý sự kiện, middleware và exception handlers
- **database**: Kết nối và tương tác với cơ sở dữ liệu
- **models**: Định nghĩa các model dữ liệu
- **routers**: Định nghĩa các API endpoints
- **utils**: Các tiện ích hỗ trợ

### 3. Kết nối cơ sở dữ liệu (database/db.py)
- Thiết lập kết nối đến PostgreSQL sử dụng SQLAlchemy
- Định nghĩa hàm dependency `get_db()` để cung cấp session cho các route
- Định nghĩa models SQLAlchemy cho dữ liệu sách
- Tự động đóng connection sau khi sử dụng

### 4. Models dữ liệu (models/book.py)
- Định nghĩa model Pydantic `Book` cho dữ liệu sách
- Định nghĩa model `BookCreate` cho việc tạo sách mới
- Định nghĩa model `BookList` cho danh sách sách và thông tin phân trang
- Định nghĩa model `SearchResult` cho kết quả tìm kiếm
- Định nghĩa model `BatchBookResult` cho việc thêm nhiều sách

### 5. Cấu hình hệ thống (config/settings.py)
- Định nghĩa các lớp cấu hình (DBSettings, SearchSettings, AppSettings)
- Sử dụng singleton pattern để quản lý cấu hình
- Thiết lập logging và các tham số mặc định

### 6. API Endpoints (routers/books.py)

#### 6.1 Lấy danh sách sách (`GET /books/`)
- Nhận tham số: limit, offset, title (tùy chọn), category (tùy chọn)
- Tham số limit quy định số lượng sách trả về
- Tham số offset dùng cho phân trang
- Tham số title dùng để lọc theo tiêu đề
- Tham số category dùng để lọc theo danh mục sách
- Truy vấn database và trả về danh sách sách theo các tiêu chí

#### 6.2 Lấy chi tiết một cuốn sách (`GET /books/{book_id}`)
- Nhận tham số path: book_id
- Truy vấn database với ID cụ thể
- Trả về thông tin đầy đủ của sách hoặc 404 nếu không tìm thấy

#### 6.3 Tạo sách mới (`POST /books/`)
- Nhận dữ liệu sách từ request body
- Tạo bản ghi mới trong database
- Trả về thông tin sách đã tạo

#### 6.4 Thêm nhiều sách cùng lúc (`POST /books/batch`)
- Nhận danh sách sách từ request body
- Thêm từng sách vào database
- Trả về kết quả với số lượng thành công/thất bại

#### 6.5 Tìm kiếm sách theo tiêu đề (`GET /books/search/title`)
- Nhận tham số: keyword, limit, offset, category (tùy chọn)
- Truy vấn database với điều kiện ILIKE %keyword% trên cột title
- Có thể lọc thêm theo danh mục sách
- Trả về kết quả tìm kiếm và thông tin phân trang

#### 6.6 Tìm kiếm sách theo tác giả (`GET /books/search/author`)
- Nhận tham số: keyword, limit, offset, category (tùy chọn)
- Truy vấn database với điều kiện ILIKE %keyword% trên cột author
- Có thể lọc thêm theo danh mục sách
- Trả về kết quả tìm kiếm và thông tin phân trang

#### 6.7 Tìm kiếm sách theo danh mục (`GET /books/search/category`)
- Nhận tham số: category, limit, offset
- Truy vấn database với điều kiện chính xác trên cột category
- Trả về danh sách sách thuộc danh mục và thông tin phân trang

## Đặc điểm kỹ thuật

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Xử lý JSON**: Pydantic
- **CORS**: Hỗ trợ cross-origin requests
- **Phân trang**: Hỗ trợ thông qua tham số limit và offset
- **Tìm kiếm**: Hỗ trợ tìm kiếm theo tiêu đề, tác giả, hoặc danh mục
- **Lọc**: Hỗ trợ lọc theo danh mục kết hợp với tìm kiếm
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
      "image_url": "https://cdn1.fahasa.com/media/catalog/product/image_195509_1_36793.jpg",
      "category": "van-hoc-trong-nuoc"
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
  "image_url": "https://cdn1.fahasa.com/media/catalog/product/image_195509_1_36793.jpg",
  "category": "van-hoc-trong-nuoc"
}
```

## Danh mục sách hỗ trợ

API hỗ trợ các danh mục sách sau:
- `van-hoc-trong-nuoc`: Văn học trong nước
- `kinh-te`: Kinh tế - Chính trị - Pháp lý
- `tam-ly-ky-nang-song`: Tâm lý - Kỹ năng sống
- `nuoi-day-con`: Nuôi dạy con
- `sach-hoc-ngoai-ngu`: Sách học ngoại ngữ

## Cách chạy API

1. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```

2. Chạy API:
   ```
   python -m api.main
   ```
   
   Hoặc sử dụng uvicorn trực tiếp:
   ```
   uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
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

5. Lấy sách thuộc danh mục "kinh-te":
   ```
   GET /books/search/category?category=kinh-te&limit=10&offset=0
   ```

6. Tìm kiếm sách có tiêu đề chứa "kim" thuộc danh mục "van-hoc-trong-nuoc":
   ```
   GET /books/search/title?keyword=kim&category=van-hoc-trong-nuoc&limit=10&offset=0
   ```

7. Lọc sách theo danh mục trong API chính:
   ```
   GET /books/?category=tam-ly-ky-nang-song&limit=10&offset=0
   ```

## Cấu trúc dự án

```
api/
├── __init__.py       # Package initialization
├── main.py           # Entry point của ứng dụng FastAPI
├── clean_old_files.py# Script dọn dẹp tệp cũ
├── config/           # Cấu hình, hằng số
│   ├── __init__.py
│   └── settings.py
├── core/             # Core modules
│   ├── __init__.py
│   ├── events.py     # App events (startup, shutdown)
│   ├── middleware.py # Middleware configuration
│   └── exceptions.py # Exception handlers
├── database/         # Kết nối và xử lý database
│   ├── __init__.py
│   └── db.py
├── models/           # Pydantic models
│   ├── __init__.py
│   └── book.py
├── routers/          # API endpoints
│   ├── __init__.py
│   └── books.py
├── utils/            # Utilities
│   ├── __init__.py
│   ├── clean_pycache.py
│   └── logging.py
├── requirements.txt  # Project dependencies
└── README.md         # Tài liệu dự án
```

## API Endpoints

- `GET /books`: Lấy danh sách sách với phân trang và lọc theo danh mục
- `GET /books/{book_id}`: Lấy thông tin sách theo ID
- `POST /books`: Thêm một cuốn sách mới
- `POST /books/batch`: Thêm nhiều cuốn sách cùng lúc
- `GET /books/search/title`: Tìm kiếm sách theo tiêu đề, có thể lọc theo danh mục
- `GET /books/search/author`: Tìm kiếm sách theo tác giả, có thể lọc theo danh mục
- `GET /books/search/category`: Tìm kiếm sách theo danh mục

## Dọn dẹp tệp Python cache

Để xóa các tệp cache Python (`__pycache__` và `.pyc`), sử dụng script `clean_pycache.py`:

```
python -m api.utils.clean_pycache --dir api
```

## Dọn dẹp tệp cũ

Để xóa các tệp cũ sau khi tái cấu trúc, sử dụng script `clean_old_files.py`:

```
python -m api.clean_old_files
```

Để chỉ xem các tệp sẽ bị xóa mà không thực sự xóa:

```
python -m api.clean_old_files --dry-run
``` 