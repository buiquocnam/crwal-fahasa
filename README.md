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
   - Truy cập nhiều URL từ Fahasa.com cho các danh mục sách khác nhau:
     - Văn học trong nước: `https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc.html`
     - Kinh tế: `https://www.fahasa.com/sach-trong-nuoc/kinh-te-chinh-tri-phap-ly.html`
     - Tâm lý - Kỹ năng sống: `https://www.fahasa.com/sach-trong-nuoc/tam-ly-ky-nang-song.html`
     - Nuôi dạy con: `https://www.fahasa.com/sach-trong-nuoc/nuoi-day-con.html`
     - Sách học ngoại ngữ: `https://www.fahasa.com/sach-trong-nuoc/sach-hoc-ngoai-ngu.html`
   - Thu thập thông tin sách: tên, tác giả, giá, giá gốc, phần trăm giảm giá, URL sách, URL ảnh, danh mục
   - Lưu dữ liệu vào các file JSON trong thư mục `/data`, cả dạng riêng lẻ theo danh mục và tổng hợp

2. **Ingestion** xử lý dữ liệu:
   - Đợi Crawler thu thập dữ liệu xong
   - Đọc dữ liệu từ file JSON
   - Tạo schema trong PostgreSQL nếu chưa tồn tại
   - Chuẩn hóa dữ liệu trước khi nhập
   - Nhập dữ liệu vào bảng `books` (bao gồm thông tin danh mục)

3. **API** (FastAPI) cung cấp endpoints:
   - `/books` - Lấy danh sách sách với phân trang và lọc theo danh mục
   - `/books/{id}` - Lấy thông tin chi tiết của một sách
   - `/books/search/title` - Tìm kiếm sách theo tiêu đề
   - `/books/search/author` - Tìm kiếm sách theo tác giả
   - `/books/search/category` - Tìm kiếm sách theo danh mục

4. **Web UI** hiển thị giao diện:
   - Trang chủ có form tìm kiếm
   - Hiển thị kết quả tìm kiếm với hình ảnh, giá, tác giả
   - Hỗ trợ phân trang kết quả

5. **Nginx** làm API Gateway:
   - Proxy trực tiếp đến endpoint `/books/*`
   - Chuyển tiếp tất cả các request khác đến API service

## Quy trình khởi chạy

Khi khởi động bằng `docker-compose up`, các container sẽ khởi động theo thứ tự:

1. **PostgreSQL** khởi động trước (với healthcheck)
2. **Crawler** bắt đầu thu thập dữ liệu (đợi PostgreSQL healthy)
3. **Ingestion** đợi Crawler hoàn thành và đưa dữ liệu vào PostgreSQL
4. **API** khởi động (đợi PostgreSQL healthy)
5. **Web UI** khởi động (đợi API sẵn sàng, tùy cấu hình)
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

## Cách truy cập API

### API Endpoints:
- API qua Nginx (proxy): `http://localhost:8080/books/`
- API trực tiếp tới container: `http://localhost:8001/books`

### Các tham số truy vấn:
- Lấy sách phân trang: `/books?limit=10&offset=20`
- Lọc theo danh mục: `/books?category=van-hoc-trong-nuoc&limit=10` 
- Tìm kiếm theo tiêu đề: `/books/search/title?keyword=kim&limit=10`
- Tìm kiếm theo tác giả: `/books/search/author?keyword=nguyen&limit=10`
- Tìm kiếm theo danh mục: `/books/search/category?category=kinh-te&limit=10`

### Ví dụ các API call:
1. Lấy 10 sách đầu tiên:
   ```
   GET http://localhost:8080/books/?limit=10&offset=0
   ```

2. Lấy chi tiết sách có ID=1:
   ```
   GET http://localhost:8080/books/1
   ```

3. Tìm kiếm sách có tiêu đề chứa từ "kim":
   ```
   GET http://localhost:8080/books/search/title?keyword=kim&limit=10&offset=0
   ```

4. Tìm kiếm sách của tác giả có tên chứa "nguyen":
   ```
   GET http://localhost:8080/books/search/author?keyword=nguyen&limit=10&offset=0
   ```

5. Tìm kiếm sách thuộc danh mục "kinh-te":
   ```
   GET http://localhost:8080/books/search/category?category=kinh-te&limit=10&offset=0
   ```

6. Kết hợp tìm kiếm theo tác giả và lọc theo danh mục:
   ```
   GET http://localhost:8080/books/search/author?keyword=nguyen&category=van-hoc-trong-nuoc&limit=10
   ```

## Danh sách danh mục sách
Hệ thống hiện hỗ trợ các danh mục sách sau:
- `van-hoc-trong-nuoc`: Văn học trong nước
- `kinh-te`: Kinh tế - Chính trị - Pháp lý
- `tam-ly-ky-nang-song`: Tâm lý - Kỹ năng sống
- `nuoi-day-con`: Nuôi dạy con
- `sach-hoc-ngoai-ngu`: Sách học ngoại ngữ

## Tài liệu chi tiết các thành phần

Mỗi thành phần của hệ thống đều có tài liệu riêng mô tả chi tiết:

- **Crawler**: [crawler/README.md](crawler/README.md) - Mô tả quy trình thu thập dữ liệu
- **Ingestion**: [ingestion/README.md](ingestion/README.md) - Mô tả quy trình nhập dữ liệu vào PostgreSQL
- **API**: [api/README.md](api/README.md) - Mô tả các endpoints và cách sử dụng API
- **Nginx**: [nginx.conf.README.md](nginx.conf.README.md) - Mô tả cấu hình và vai trò của Nginx

## Cấu trúc dự án

```
fahasa_crawler/
├── crawler/                 # Mã nguồn crawler
│   ├── crawler.py           # Script crawl dữ liệu
│   ├── README.md            # Tài liệu mô tả crawler
│   └── requirements.txt     # Thư viện Python cần thiết
├── ingestion/               # Mã nguồn ingestion
│   ├── ingestion.py         # Script nhập dữ liệu vào PostgreSQL
│   ├── README.md            # Tài liệu mô tả ingestion
│   └── requirements.txt     # Thư viện Python cần thiết
├── api/                     # Mã nguồn API
│   ├── config.py            # Cấu hình và hằng số
│   ├── database.py          # Xử lý kết nối database
│   ├── main.py              # Entry point của FastAPI app
│   ├── models.py            # Pydantic models
│   ├── books.py             # Routers và endpoints
│   ├── README.md            # Tài liệu mô tả API
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
├── nginx.conf.README.md     # Tài liệu mô tả Nginx
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

### Lỗi 404 khi truy cập API
- Đảm bảo URL đúng định dạng (để ý dấu `/` ở cuối URL)
- Kiểm tra cấu hình Nginx trong file nginx.conf
- Kiểm tra logs để tìm nguyên nhân: `docker-compose logs -f nginx`

### Lỗi kết nối từ Web đến API
- Kiểm tra biến `API_URL` trong file web.py
- Đảm bảo tất cả services kết nối đến cùng mạng Docker 
- Xem logs của web: `docker-compose logs -f web`