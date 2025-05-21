# Web Giao Diện Fahasa

Ứng dụng web Flask cung cấp giao diện người dùng đẹp mắt và thân thiện để tìm kiếm, duyệt và khám phá sách từ API Fahasa.

## Tính năng chính

- 🔍 **Tìm kiếm đa năng**: Tìm sách theo tên hoặc tác giả với kết quả tức thì
- 📚 **Duyệt theo danh mục**: Khám phá sách theo danh mục
- 📖 **Chi tiết sách**: Xem thông tin chi tiết của từng cuốn sách
- 📱 **Responsive**: Tối ưu hiển thị trên mọi thiết bị
- 🔄 **Kết nối API**: Tích hợp mượt mà với API Fahasa
- 🚀 **Hiệu suất cao**: Tải trang nhanh chóng, trải nghiệm mượt mà
- 🛡️ **Xử lý lỗi**: Hệ thống xử lý lỗi toàn diện

## Công nghệ sử dụng

- **[Flask]**: Framework web nhẹ và linh hoạt
- **[Bootstrap 5]**: Framework CSS hiện đại
- **[Requests]**: Thư viện HTTP Python
- **[Jinja2]**: Template engine mạnh mẽ
- **[JavaScript]**: Tăng cường trải nghiệm người dùng
- **[Docker]**: Container hóa ứng dụng


## Cấu trúc dự án

```
web/
├── main.py                 # Entry point ứng dụng
├── requirements.txt        # Thư viện cần thiết
├── Dockerfile              # Cấu hình Docker
├── templates/              # Templates HTML
│   ├── index.html          # Template chính
│   ├── utils.html          # Hàm tiện ích Jinja
│   ├── static/             # Tài nguyên tĩnh (CSS, JS, images)
│   └── partials/           # Các thành phần template
├── models/                 # Models dữ liệu
│   └── book.py             # Model Book tương tác với API
├── controllers/            # Xử lý logic nghiệp vụ
│   └── book_controller.py  # Điều khiển các tác vụ liên quan đến sách
├── utils/                  # Tiện ích
│   └── api_utils.py        # Các hàm tiện ích tương tác API
└── config/                 # Cấu hình
    └── settings.py         # Thiết lập ứng dụng
```

## Các trang giao diện

### Trang chủ
- Hiển thị hero section hấp dẫn
- Danh sách danh mục phổ biến
- Danh sách sách mới nhất
- Form tìm kiếm nổi bật

### Tìm kiếm
- Tìm kiếm theo tên sách hoặc tác giả
- Hiển thị kết quả với phân trang
- Lọc theo danh mục sách

### Chi tiết sách
- Hiển thị đầy đủ thông tin sách
- Hình ảnh, giá, tác giả, nhà xuất bản, v.v.
- Mô tả chi tiết sách

## API Endpoints được sử dụng

Ứng dụng giao tiếp với API Fahasa thông qua các endpoints sau:

- `GET /books`: Lấy danh sách sách với phân trang và lọc
- `GET /books/{book_id}`: Lấy thông tin chi tiết sách
- `GET /books/categories/list`: Lấy danh sách danh mục sách

## Các tính năng UI/UX

- **Hiệu ứng chuyển động**: Sử dụng Animate.css cho các chuyển động mượt mà
- **Breadcrumb**: Điều hướng dễ dàng giữa các trang
- **Phân trang**: Điều hướng qua nhiều trang kết quả
- **Responsive**: Giao diện tối ưu trên điện thoại, máy tính bảng và máy tính
- **Toast Notifications**: Thông báo với người dùng một cách nhẹ nhàng
- **Back to Top**: Nút quay về đầu trang khi cuộn xuống
- **Lịch sử tìm kiếm**: Lưu trữ các từ khóa tìm kiếm gần đây


