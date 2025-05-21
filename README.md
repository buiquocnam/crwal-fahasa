# 📚 Hệ Thống Thu Thập và Hiển Thị Dữ Liệu Sách Fahasa

Dự án này xây dựng hệ thống hoàn chỉnh để thu thập dữ liệu sách từ Fahasa.com, lưu trữ vào cơ sở dữ liệu PostgreSQL, cung cấp API truy vấn dữ liệu, và giao diện web thân thiện để người dùng tìm kiếm và khám phá sách.

## 🏗️ Kiến trúc hệ thống

![Fahasa System Architecture](https://i.imgur.com/nCkRdUh.png)

Hệ thống bao gồm 5 thành phần chính:

1. **🕷️ Crawler Service**: Thu thập dữ liệu sách từ Fahasa.com
2. **🔄 Ingestion Service**: Xử lý và nhập dữ liệu vào PostgreSQL
3. **🚀 API Service**: Cung cấp REST API để truy vấn dữ liệu sách
4. **🖥️ Web UI**: Giao diện người dùng để tìm kiếm và duyệt sách
5. **🔀 Nginx**: API Gateway và reverse proxy cho hệ thống

## ⚙️ Luồng hoạt động

```
Luồng dữ liệu: Fahasa Website → Crawler → JSON Files → Ingestion → PostgreSQL → API
Luồng người dùng: User → Nginx → [Web UI / API] → PostgreSQL
```

1. **Crawler**:
   - Thu thập dữ liệu từ nhiều danh mục sách
   - Xử lý đa luồng cho hiệu suất cao
   - Lưu trữ dữ liệu vào các file JSON

2. **Ingestion**:
   - Nhận thông báo từ Crawler khi có dữ liệu mới
   - Đọc, xác thực và chuẩn hóa dữ liệu
   - Nhập dữ liệu vào PostgreSQL

3. **API**:
   - Cung cấp endpoints để truy vấn dữ liệu
   - Hỗ trợ tìm kiếm theo tiêu đề, tác giả, danh mục
   - Phân trang và lọc kết quả

4. **Nginx**:
   - Hoạt động như API Gateway
   - Chuyển tiếp yêu cầu đến các dịch vụ phù hợp
   - Cung cấp layer bảo mật và load balancing

5. **Web UI**:
   - Giao diện thân thiện, responsive
   - Tìm kiếm và duyệt sách dễ dàng
   - Hiển thị thông tin chi tiết về sách

## 🚀 Cách chạy hệ thống

### Yêu cầu tiên quyết
- Docker và Docker Compose
- Kết nối internet (để crawler lấy dữ liệu)

### Khởi động toàn bộ hệ thống
```bash
docker-compose up --build
```

### Truy cập các dịch vụ
- **Web UI**: http://localhost:8000
- **API (qua Nginx)**: http://localhost:8080/books
- **API (trực tiếp)**: http://localhost:8001/books
- **Crawler API**: http://localhost:8002
- **Ingestion API**: http://localhost:8003

## 🔍 Các danh mục sách hỗ trợ

Hệ thống thu thập dữ liệu từ các danh mục sách sau:

- `van-hoc-trong-nuoc`: Văn học trong nước
- `kinh-te`: Kinh tế - Chính trị - Pháp lý
- `tam-ly-ky-nang-song`: Tâm lý - Kỹ năng sống
- `nuoi-day-con`: Nuôi dạy con
- `sach-hoc-ngoai-ngu`: Sách học ngoại ngữ

## 📡 API Endpoints

### 1. Lấy danh sách sách
```
GET /books/?limit=10&page=1
```

### 2. Lấy chi tiết sách
```
GET /books/{book_id}
```

### 3. Tìm kiếm sách
```
GET /books/?title=nhà giả kim&limit=10&page=1
GET /books/?author=paulo&limit=10&page=1
GET /books/?category=van-hoc-trong-nuoc&limit=10&page=1
```

### 4. Lấy danh sách danh mục
```
GET /books/categories/list
```

## 📂 Cấu trúc dự án

```
project/
├── data_crawling/        # Thu thập dữ liệu từ Fahasa
├── data_ingestion/       # Nhập dữ liệu vào PostgreSQL
├── database_api/         # API truy vấn dữ liệu
├── web/                  # Giao diện người dùng
├── data/                 # Thư mục lưu dữ liệu JSON (tạo tự động)
├── docker-compose.yml    # Cấu hình Docker Compose
├── nginx.conf            # Cấu hình Nginx API Gateway
└── README.md             # Tài liệu này
```

## 📄 Tài liệu chi tiết các thành phần

Mỗi thành phần đều có tài liệu riêng chi tiết:

- [**🕷️ Dịch vụ Crawler**](data_crawling/README.md): Thu thập dữ liệu sách từ Fahasa
- [**🔄 Dịch vụ Ingestion**](data_ingestion/README.md): Nhập dữ liệu vào cơ sở dữ liệu
- [**🚀 API Service**](database_api/README.md): Cung cấp REST API
- [**🖥️ Web UI**](web/README.md): Giao diện người dùng

## 🛠️ Gỡ lỗi và khắc phục sự cố

### Vấn đề Crawler
- Kiểm tra logs: `docker-compose logs data_crawling`
- Truy cập API: `http://localhost:8002/`

### Vấn đề Ingestion
- Kiểm tra logs: `docker-compose logs data_ingestion`
- Truy cập API: `http://localhost:8003/`

### Vấn đề với PostgreSQL
- Kiểm tra logs: `docker-compose logs postgres`
- Kết nối trực tiếp: `docker exec -it postgres psql -U fahasa -d fahasa_db`

### Vấn đề với API
- Kiểm tra logs: `docker-compose logs database_api`
- Truy cập trực tiếp: `http://localhost:8001/books/`

### Vấn đề với Nginx
- Kiểm tra logs: `docker-compose logs nginx`
- Kiểm tra cấu hình: `cat nginx.conf`
- Xác minh proxy hoạt động: `curl http://localhost:8080/health`

### Vấn đề với Web UI
- Kiểm tra logs: `docker-compose logs web`
- Kiểm tra kết nối API trong cấu hình

