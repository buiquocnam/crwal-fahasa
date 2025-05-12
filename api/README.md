# Fahasa Book API

API để truy vấn dữ liệu sách từ Fahasa

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