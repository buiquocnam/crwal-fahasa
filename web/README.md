# Dịch Vụ Web Fahasa

Ứng dụng web dựa trên Flask cung cấp giao diện người dùng để duyệt và tìm kiếm sách từ API Fahasa.

## Cấu Trúc Dự Án

```
web/
├── app.py                 # Điểm khởi đầu của ứng dụng
├── requirements.txt       # Các thư viện Python cần thiết
├── config/               # Thư mục cấu hình
│   └── settings.py       # Cài đặt ứng dụng
├── controllers/          # Controllers
│   └── book_controller.py # Xử lý các request liên quan đến sách
├── models/              # Models
│   └── book.py          # Model dữ liệu sách
├── utils/               # Các tiện ích
│   └── api_utils.py     # Các tiện ích liên quan đến API
└── templates/           # Templates HTML
    └── index.html       # Template chính
```

## Tính Năng

- Duyệt tất cả sách với phân trang
- Tìm kiếm sách theo tiêu đề hoặc tác giả
- Xem thông tin chi tiết sách
- Giao diện web responsive
- Xử lý lỗi và ghi log

## Yêu Cầu Hệ Thống

- Python 3.9 trở lên
- Docker (tùy chọn, cho triển khai container)

## Cài Đặt

1. Clone repository:
```bash
git clone <repository-url>
cd web
```

2. Tạo và kích hoạt môi trường ảo (khuyến nghị):
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Cấu Hình

Ứng dụng có thể được cấu hình thông qua các biến môi trường:

- `API_URL`: URL của API Fahasa (mặc định: "http://fahasa_api:8000")
- `FLASK_HOST`: Host chạy ứng dụng (mặc định: "0.0.0.0")
- `FLASK_PORT`: Port chạy ứng dụng (mặc định: 8000)
- `FLASK_DEBUG`: Chế độ debug (mặc định: False)

## Chạy Ứng Dụng

### Phát Triển Local

```bash
python app.py
```

Ứng dụng sẽ có sẵn tại `http://localhost:8000`

### Triển Khai Docker

1. Build Docker image:
```bash
docker build -t fahasa-web -f Dockerfile.web .
```

2. Chạy container:
```bash
docker run -p 8000:8000 fahasa-web
```

## Tích Hợp API

Dịch vụ web tích hợp với API Fahasa thông qua các endpoint sau:

- `GET /books`: Liệt kê tất cả sách với phân trang
- `GET /books/search/title`: Tìm kiếm sách theo tiêu đề
- `GET /books/search/author`: Tìm kiếm sách theo tác giả
- `GET /books/{id}`: Lấy thông tin chi tiết sách theo ID

## Xử Lý Lỗi

Ứng dụng bao gồm xử lý lỗi toàn diện:

- Lỗi kết nối API
- Tham số tìm kiếm không hợp lệ
- Dữ liệu sách bị thiếu
- Lỗi server

Tất cả lỗi được ghi log và hiển thị cho người dùng theo định dạng thân thiện.

## Ghi Log

Ứng dụng sử dụng module logging của Python với cấu hình sau:

- Cấp độ log: INFO
- Định dạng: `%(asctime)s - %(levelname)s - %(message)s`
- Đầu ra: Console

## Phát Triển

### Thêm Tính Năng Mới

1. Tạo model mới trong thư mục `models/`
2. Thêm controller tương ứng trong thư mục `controllers/`
3. Cập nhật templates trong thư mục `templates/`
4. Thêm routes mới trong `app.py`

### Kiểm Thử

Để thêm kiểm thử:

1. Tạo file test trong thư mục `tests/`
2. Sử dụng pytest cho việc kiểm thử
3. Chạy test với lệnh:
```bash
pytest
```
