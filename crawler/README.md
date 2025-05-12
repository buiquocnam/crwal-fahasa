# Fahasa Book Crawler

Crawler này thu thập dữ liệu sách từ trang Fahasa.com, đặc biệt là mục "Văn học trong nước". Dữ liệu thu thập bao gồm tiêu đề, tác giả, giá, giá gốc, phần trăm giảm giá, URL sách và URL hình ảnh.

## Quy trình hoạt động

### 1. Khởi tạo
- Thiết lập logging để ghi nhật ký quá trình
- Định nghĩa hằng số: URL gốc, thư mục đầu ra, tên file đầu ra, số trang tối đa (MAX_PAGES)

### 2. Lấy nội dung trang (hàm `get_page`)
- Gửi request HTTP GET đến URL của Fahasa
- Sử dụng headers giả lập trình duyệt để tránh bị chặn
- Thiết lập encoding utf-8 để hỗ trợ tiếng Việt
- Có cơ chế thử lại tối đa 3 lần nếu request thất bại
- Trả về nội dung HTML của trang

### 3. Phân tích dữ liệu sách (hàm `parse_books`)
- Sử dụng BeautifulSoup để phân tích HTML
- Tìm container chứa danh sách sách (`ul#products_grid.products-grid`)
- Tìm tất cả các mục sách (`li`) trong container
- Với mỗi mục sách, trích xuất:
  - Tiêu đề (`h2.product-name-no-ellipsis a` hoặc `a.product-image`)
  - Tác giả (`div.product-author span`)
  - Giá hiện tại (`p.special-price span.price` hoặc `span.price`)
  - Giá gốc (`p.old-price span.price`)
  - Phần trăm giảm giá (`span.discount-percent`)
  - URL sách (thuộc tính `href` của thẻ a)
  - URL hình ảnh (thuộc tính `data-src` hoặc `src` của thẻ img)
- Tạo dictionary chứa thông tin sách và thêm vào danh sách kết quả

### 4. Lấy URL trang tiếp theo (hàm `get_next_page_url`)
- Tìm phần phân trang (`div.pages`)
- Tìm nút "Next" thông qua thuộc tính onclick chứa "catalog_ajax.Page_change('next')"
- Nếu tìm thấy, lấy số trang hiện tại và tính số trang tiếp theo
- Tạo URL cho trang tiếp theo dạng `base_url?p=next_page`

### 5. Quy trình thu thập (hàm `crawl_fahasa`)
- Bắt đầu từ URL gốc (`BASE_URL`)
- Vòng lặp đến khi đủ số trang hoặc không còn trang tiếp theo:
  - Lấy nội dung trang bằng `get_page`
  - Phân tích và trích xuất thông tin sách bằng `parse_books`
  - Thêm kết quả vào danh sách tổng hợp
  - Tìm URL trang tiếp theo bằng `get_next_page_url`
  - Nếu tìm thấy URL trang tiếp theo, tiếp tục; nếu không, thử tạo URL bằng cách tăng số trang
  - Chờ 2 giây trước khi lấy trang tiếp theo (để tránh tải quá nhiều trong thời gian ngắn)
- Trả về danh sách tất cả sách đã thu thập

### 6. Lưu dữ liệu (hàm `save_to_json`)
- Tạo thư mục đầu ra nếu chưa tồn tại
- Ghi dữ liệu vào file JSON với định dạng UTF-8 để hỗ trợ tiếng Việt
- Sử dụng `ensure_ascii=False` để đảm bảo hiển thị đúng ký tự tiếng Việt

### 7. Hàm chính (hàm `main`)
- Chờ 5 giây để đảm bảo mạng khả dụng (đặc biệt trong môi trường Docker)
- Gọi `crawl_fahasa` để thu thập dữ liệu
- Gọi `save_to_json` để lưu kết quả
- Xử lý ngoại lệ và ghi log nếu có lỗi

## Các tham số có thể tùy chỉnh

- `BASE_URL`: URL mục sách cần thu thập
- `OUTPUT_DIR`: Thư mục lưu file JSON
- `OUTPUT_FILE`: Đường dẫn đầy đủ của file kết quả
- `MAX_PAGES`: Số trang tối đa cần thu thập (mặc định: 5)

## Cách chạy crawler

1. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```

2. Chạy crawler:
   ```
   python crawler.py
   ```

## Cách chạy trong Docker

1. Xây dựng image Docker:
   ```
   docker build -t fahasa-crawler -f Dockerfile.crawler .
   ```

2. Chạy container:
   ```
   docker run -v ./data:/app/data fahasa-crawler
   ```

## Dữ liệu đầu ra

File JSON có định dạng:
```json
[
  {
    "title": "Tên sách",
    "author": "Tên tác giả",
    "price": "79.000đ",
    "original_price": "100.000đ",
    "discount": "-20%",
    "url": "https://www.fahasa.com/nha-gia-kim.html",
    "image_url": "https://cdn1.fahasa.com/media/catalog/product/image_195509_1_36793.jpg"
  },
  // Các sách khác...
]
``` 