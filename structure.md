project/
├── data/                  # Thư mục chứa dữ liệu JSON
├── data_crawling/         # Thu thập dữ liệu từ Fahasa
│   ├── src/
│   │   ├── config/
│   │   │   ├── crawler_config.json
│   │   │   └── settings.py
│   │   ├── crawlers/
│   │   │   ├── crawler_runner.py
│   │   │   ├── fahasa_crawler.py
│   │   │   └── scheduler.py
│   │   ├── parsers/
│   │   │   └── book_parser.py
│   │   ├── utils/
│   │   │   ├── file_utils.py
│   │   │   └── html_fetcher.py
│   │   └── __init__.py
│   ├── Dockerfile
│   ├── main.py
│   ├── README.md
│   └── requirements.txt
├── data_ingestion/        # Nhập dữ liệu vào PostgreSQL
│   ├── src/
│   │   ├── api/
│   │   │   └── book_client.py
│   │   ├── config/
│   │   │   └── settings.py
│   │   ├── utils/
│   │   │   └── data_loader.py
│   │   ├── validation/
│   │   │   ├── schema.py
│   │   │   └── validator.py
│   │   ├── ingestion.py
│   │   └── __init__.py
│   ├── Dockerfile
│   ├── main.py
│   ├── README.md
│   └── requirements.txt
├── database_api/          # API truy vấn dữ liệu
│   ├── src/
│   │   ├── config/
│   │   │   └── settings.py
│   │   ├── database/
│   │   │   └── init_db.py
│   │   ├── models/
│   │   │   └── book.py
│   │   ├── repositories/
│   │   │   └── book_repository.py
│   │   ├── routers/
│   │   │   └── book_router.py
│   │   └── services/
│   │       └── book_service.py
│   ├── Dockerfile
│   ├── main.py
│   ├── README.md
│   └── requirements.txt
├── web/                   # Giao diện người dùng
│   ├── config/
│   │   └── settings.py
│   ├── controllers/
│   │   └── book_controller.py
│   ├── models/
│   │   └── book.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── utils.html
│   │   ├── partials/
│   │   │   ├── book_card.html
│   │   │   ├── book_detail.html
│   │   │   ├── book_list.html
│   │   │   ├── categories_list.html
│   │   │   └── toast.html
│   │   └── static/
│   │       ├── css/
│   │       └── js/
│   ├── utils/
│   │   └── api_utils.py
│   ├── Dockerfile
│   ├── main.py
│   ├── README.md
│   └── requirements.txt
├── static/                # Thư mục chứa tài nguyên tĩnh
├── docker-compose.yml     # Cấu hình Docker Compose
├── nginx.conf             # Cấu hình Nginx API Gateway
├── .gitignore             # Cấu hình Git ignore
└── README.md              # Tài liệu chính
