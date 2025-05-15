# Fahasa Book Crawler

Crawler này thu thập dữ liệu sách từ nhiều danh mục của trang Fahasa.com, bao gồm Văn học trong nước, Kinh tế, Tâm lý - Kỹ năng sống, và các danh mục khác. Dữ liệu thu thập bao gồm tiêu đề, tác giả, giá, giá gốc, phần trăm giảm giá, URL sách, URL hình ảnh và danh mục.

## Quy trình hoạt động

### 1. Khởi tạo
- Thiết lập logging để ghi nhật ký quá trình
- Định nghĩa danh sách các URL theo danh mục sách trong `BOOK_CATEGORIES`
- Định nghĩa hằng số: thư mục đầu ra, số trang tối đa cho mỗi danh mục (MAX_PAGES)

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
- Bổ sung thông tin danh mục (`category`) cho mỗi sách

### 4. Lấy URL trang tiếp theo (hàm `get_next_page_url`)
- Tìm phần phân trang (`div.pages`)
- Tìm nút "Next" thông qua thuộc tính onclick chứa "catalog_ajax.Page_change('next')"
- Nếu tìm thấy, lấy số trang hiện tại và tính số trang tiếp theo
- Tạo URL cho trang tiếp theo dạng `base_url?p=next_page`

### 5. Quy trình thu thập từng danh mục (hàm `crawl_category`)
- Nhận URL danh mục và tên danh mục
- Vòng lặp đến khi đủ số trang hoặc không còn trang tiếp theo:
  - Lấy nội dung trang bằng `get_page`
  - Phân tích và trích xuất thông tin sách bằng `parse_books`
  - Thêm kết quả vào danh sách tổng hợp
  - Tìm URL trang tiếp theo bằng `get_next_page_url`
  - Nếu tìm thấy URL trang tiếp theo, tiếp tục; nếu không, thử tạo URL bằng cách tăng số trang
  - Chờ 2 giây trước khi lấy trang tiếp theo (để tránh tải quá nhiều trong thời gian ngắn)
- Trả về danh sách tất cả sách đã thu thập từ danh mục

### 6. Lưu dữ liệu (hàm `save_to_json`)
- Tạo thư mục đầu ra nếu chưa tồn tại
- Ghi dữ liệu vào file JSON với định dạng UTF-8 để hỗ trợ tiếng Việt
- Sử dụng `ensure_ascii=False` để đảm bảo hiển thị đúng ký tự tiếng Việt

### 7. Hàm chính (hàm `main`)
- Chờ 5 giây để đảm bảo mạng khả dụng (đặc biệt trong môi trường Docker)
- Khởi tạo danh sách tổng hợp tất cả sách
- Lặp qua mỗi danh mục trong `BOOK_CATEGORIES`:
  - Tạo đường dẫn file JSON riêng cho danh mục
  - Gọi `crawl_category` để thu thập dữ liệu cho danh mục
  - Lưu dữ liệu danh mục vào file JSON riêng
  - Thêm sách từ danh mục này vào danh sách tổng hợp
  - Chờ 3 giây trước khi chuyển sang danh mục tiếp theo
- Lưu tất cả dữ liệu vào một file JSON tổng hợp
- Xử lý ngoại lệ và ghi log nếu có lỗi

## Danh mục sách hỗ trợ

Crawler hỗ trợ các danh mục sách sau:
- `van-hoc-trong-nuoc`: Văn học trong nước
- `kinh-te`: Kinh tế - Chính trị - Pháp lý
- `tam-ly-ky-nang-song`: Tâm lý - Kỹ năng sống
- `nuoi-day-con`: Nuôi dạy con
- `sach-hoc-ngoai-ngu`: Sách học ngoại ngữ

## Các tham số có thể tùy chỉnh

- `BOOK_CATEGORIES`: Dictionary chứa các danh mục sách và URL tương ứng
- `OUTPUT_DIR`: Thư mục lưu file JSON
- `MAX_PAGES`: Số trang tối đa cần thu thập cho mỗi danh mục (mặc định: 5)

## Cách thêm danh mục sách mới

Để thêm danh mục sách mới, chỉ cần bổ sung vào dictionary `BOOK_CATEGORIES` trong file crawler.py:

```python
BOOK_CATEGORIES = {
    "van-hoc-trong-nuoc": "https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc.html",
    "danh-muc-moi": "https://www.fahasa.com/duong-dan-den-danh-muc-moi.html",
    # Thêm các danh mục khác...
}
```

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

### File JSON tổng hợp (`fahasa_data.json`):
```json
[
  {
    "title": "Tên sách",
    "author": "Tên tác giả",
    "price": "79.000đ",
    "original_price": "100.000đ",
    "discount": "-20%",
    "url": "https://www.fahasa.com/nha-gia-kim.html",
    "image_url": "https://cdn1.fahasa.com/media/catalog/product/image_195509_1_36793.jpg",
    "category": "van-hoc-trong-nuoc"
  },
  // Các sách khác...
]
```

### File JSON theo danh mục (`fahasa_van-hoc-trong-nuoc.json`, `fahasa_kinh-te.json`, ...):
Mỗi danh mục sẽ có file JSON riêng với cấu trúc tương tự file tổng hợp, nhưng chỉ chứa sách thuộc danh mục đó. 