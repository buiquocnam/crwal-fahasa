# Fahasa Book Data Crawler và API

Dự án này xây dựng hệ thống thu thập dữ liệu từ Fahasa.com (trang thương mại điện tử sách tại Việt Nam), lưu trữ vào PostgreSQL, cung cấp API để truy vấn dữ liệu, và giao diện web để tìm kiếm sách.

## Kiến trúc hệ thống

![Fahasa Crawler Architecture](https://i.imgur.com/nCkRdUh.png)

Hệ thống bao gồm các thành phần sau:
- **Crawler**: Thu thập dữ liệu sách từ Fahasa.com
- **Landing Zone (JSON Files)**: Lưu trữ tạm thời dữ liệu crawl trong file JSON
- **Ingestion**: Đọc dữ liệu từ JSON và nhập vào PostgreSQL
- **PostgreSQL Database**: Lưu trữ dữ liệu sách
- **API**: Cung cấp endpoints REST API để truy vấn dữ liệu
- **Web UI**: Giao diện người dùng để tìm kiếm sách
- **Nginx**: API Gateway và reverse proxy

## Flow hoạt động

1. **Crawler** thu thập dữ liệu từ Fahasa.com:
   - Truy cập URL: `https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc.html`
   - Thu thập thông tin sách: tên, giá, tác giả, URL ảnh
   - Lưu dữ liệu vào file JSON trong thư mục `/data`

2. **Ingestion** xử lý dữ liệu:
   - Đợi Crawler thu thập dữ liệu xong
   - Đọc dữ liệu từ file JSON
   - Tạo schema trong PostgreSQL nếu chưa tồn tại
   - Nhập dữ liệu vào bảng `books`

3. **API** (FastAPI) cung cấp endpoints:
   - `/books` - Lấy danh sách sách với phân trang
   - `/books/{id}` - Lấy thông tin chi tiết của một sách
   - `/books/search/title` - Tìm kiếm sách theo tiêu đề
   - `/books/search/author` - Tìm kiếm sách theo tác giả

4. **Web UI** hiển thị giao diện:
   - Trang chủ có form tìm kiếm
   - Hiển thị kết quả tìm kiếm với hình ảnh, giá, tác giả
   - Hỗ trợ phân trang kết quả

5. **Nginx** làm API Gateway:
   - Điều hướng request đến API service qua URL `/api/*`
   - Proxy trực tiếp đến endpoint `/books/*`
   - Cung cấp giao diện web thông qua URL gốc `/`

## Quy trình khởi chạy

Khi khởi động bằng `docker-compose up`, các container sẽ khởi động theo thứ tự:

1. **PostgreSQL** khởi động trước (với healthcheck)
2. **Crawler** bắt đầu thu thập dữ liệu (đợi PostgreSQL healthy)
3. **Ingestion** đợi Crawler hoàn thành và đưa dữ liệu vào PostgreSQL
4. **API** khởi động (đợi PostgreSQL healthy)
5. **Web UI** khởi động (đợi API sẵn sàng)
6. **Nginx** làm API Gateway (đợi API sẵn sàng)

## Luồng dữ liệu

```
Fahasa Website -> Crawler -> JSON Files -> Ingestion -> PostgreSQL -> API -> [Nginx] -> User
```

## Cách chạy hệ thống

1. Đảm bảo Docker và Docker Compose đã được cài đặt
2. Mở terminal tại thư mục dự án
3. Chạy lệnh: `docker-compose up --build`
4. Đợi tất cả các container khởi động hoàn tất

## Cách truy cập API và Web

### API Endpoints:
- API (qua Nginx): `http://localhost:8000/api/books`
- API (trực tiếp qua Nginx): `http://localhost:8000/books`
- API (trực tiếp tới container): `http://localhost:8001/books`
- Các tham số:
  - Lấy sách phân trang: `/books?limit=10&offset=20`
  - Tìm kiếm theo tiêu đề: `/books/search/title?keyword=kim&limit=10`
  - Tìm kiếm theo tác giả: `/books/search/author?keyword=nguyen&limit=10`

### Web UI:
- Web UI (qua Nginx): `http://localhost:8000/`
- Web UI (trực tiếp): `http://localhost:8002/`

## Cấu trúc dự án

```
fahasa_crawler/
├── crawler/                 # Mã nguồn crawler
│   ├── crawler.py           # Script crawl dữ liệu
│   └── requirements.txt     # Thư viện Python cần thiết
├── ingestion/               # Mã nguồn ingestion
│   ├── ingestion.py         # Script nhập dữ liệu vào PostgreSQL
│   └── requirements.txt     # Thư viện Python cần thiết
├── api/                     # Mã nguồn API
│   ├── config.py            # Cấu hình và hằng số
│   ├── database.py          # Xử lý kết nối database
│   ├── main.py              # Entry point của FastAPI app
│   ├── models.py            # Pydantic models
│   ├── books.py             # Routers và endpoints
│   └── requirements.txt     # Thư viện Python cần thiết  
├── web/                     # Mã nguồn Web UI
│   ├── web.py               # Flask application
│   ├── templates/           # HTML templates
│   │   └── index.html       # Trang chủ có form tìm kiếm
│   └── requirements.txt     # Thư viện Python cần thiết
├── data/                    # Thư mục lưu dữ liệu JSON (tạo tự động)
├── Dockerfile.crawler       # Dockerfile cho crawler
├── Dockerfile.ingestion     # Dockerfile cho ingestion  
├── Dockerfile.api           # Dockerfile cho API
├── Dockerfile.web           # Dockerfile cho web UI
├── docker-compose.yml       # Cấu hình Docker Compose
├── nginx.conf               # Cấu hình Nginx API Gateway
└── README.md                # File này
```

## Gỡ lỗi và khắc phục sự cố

### Vấn đề kết nối Nginx-API
Nếu gặp lỗi 500 khi truy cập qua Nginx:
- Kiểm tra logs: `docker-compose logs -f nginx`
- Kiểm tra kết nối API: `docker-compose logs -f api`
- Đảm bảo mạng Docker hoạt động: `docker network inspect fahasa_network`

### Vấn đề với PostgreSQL
Nếu API không thể kết nối đến PostgreSQL:
- Kiểm tra logs PostgreSQL: `docker-compose logs -f postgres`
- Thử kết nối trực tiếp: `docker exec -it fahasa_postgres psql -U fahasa -d fahasa_db`