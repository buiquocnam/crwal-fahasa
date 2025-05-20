document.addEventListener('DOMContentLoaded', function() {
    // Khởi tạo tooltips
    initTooltips();
    
    // Bắt sự kiện nút back-to-top
    setupBackToTop();
    
    // Bắt sự kiện cho nút wishlist
    setupWishlistButtons();
    
    // Bắt sự kiện toggle mô tả sách
    setupDescriptionToggle();
    
    // Xử lý form tìm kiếm bằng AJAX
    setupSearchForm();
    
    // Xử lý phân trang bằng AJAX
    setupPagination();
    
    // Thiết lập hero search form
    setupHeroSearchForm();
    
    // Kiểm tra nếu đang ở trang kết quả tìm kiếm và cần scroll
    checkAndScrollToResults();
});

// Khởi tạo tooltips Bootstrap
function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Thiết lập nút back to top
function setupBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');
    if (!backToTopBtn) return;
    
    window.addEventListener('scroll', function() {
        backToTopBtn.style.display = window.pageYOffset > 300 ? 'flex' : 'none';
    });
    
    backToTopBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({top: 0, behavior: 'smooth'});
    });
}

// Thiết lập nút wishlist
function setupWishlistButtons() {
    document.querySelectorAll('.btn-wishlist').forEach(button => {
        button.addEventListener('click', toggleWishlist);
    });
}

// Hàm toggle wishlist
function toggleWishlist(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const icon = this.querySelector('i');
    if (icon.classList.contains('bi-heart')) {
        icon.classList.remove('bi-heart');
        icon.classList.add('bi-heart-fill');
        this.classList.add('active');
    } else {
        icon.classList.remove('bi-heart-fill');
        icon.classList.add('bi-heart');
        this.classList.remove('active');
    }
}

// Thiết lập toggle mô tả sách
function setupDescriptionToggle() {
    const toggleBtn = document.querySelector('.toggle-description');
    if (!toggleBtn) return;
    
    toggleBtn.addEventListener('click', function() {
        const preview = document.querySelector('.description-preview');
        const full = document.querySelector('.description-full');
        const showMore = document.querySelector('.show-more');
        const showLess = document.querySelector('.show-less');
        
        preview.classList.toggle('d-none');
        full.classList.toggle('d-none');
        showMore.classList.toggle('d-none');
        showLess.classList.toggle('d-none');
    });
}

// Thiết lập form tìm kiếm AJAX
function setupSearchForm() {
    const searchForms = document.querySelectorAll('form[action="/search"]');
    if (searchForms.length === 0) return;
    
    searchForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const keywordInput = this.querySelector('input[name="keyword"]');
            const keyword = keywordInput?.value?.trim();
            
            if (!keyword) {
                // Sử dụng toast thay vì alert
                Toast.error("Vui lòng nhập từ khóa tìm kiếm", "Lỗi tìm kiếm");
                
                // Thêm hiệu ứng rung cho input
                keywordInput.classList.add('shake-x');
                setTimeout(() => {
                    keywordInput.classList.remove('shake-x');
                }, 1000);
                
                // Focus vào input
                keywordInput.focus();
                return;
            }
            
            const searchType = this.querySelector('select[name="search_type"]')?.value || 'title';
            const resultContainer = document.getElementById('search-results');
            
            // Hiển thị trạng thái loading
            resultContainer.innerHTML = `
                <div class="text-center py-5">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Đang tải...</span>
                    </div>
                    <p class="mt-3">Đang tìm kiếm...</p>
                </div>
            `;
            
            // Tạo URL và update history
            const params = new URLSearchParams({
                keyword: keyword,
                search_type: searchType
            });
            
            const fetchUrl = `/search?${params.toString()}`;
            const historyUrl = fetchUrl; // Dùng chung URL
            
            // Update URL trên browser
            window.history.pushState({}, '', historyUrl);
            
            // Scroll to search results
            scrollToResults();
            
            // Fetch kết quả
            fetch(fetchUrl, { 
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => {
                    if (!response.ok) throw new Error('Lỗi khi tải dữ liệu');
                    return response.text();
                })
                .then(html => {
                    // Cập nhật nội dung
                    resultContainer.innerHTML = html;
                    
                    // Khởi tạo lại các sự kiện sau khi nội dung được cập nhật
                    setupWishlistButtons();
                    
                    // Scroll to the top of results
                    scrollToResults();
                    
                    // Hiển thị thông báo thành công nếu có kết quả
                    const items = resultContainer.querySelectorAll('.card');
                    if (items.length > 0) {
                        Toast.success(`Đã tìm thấy ${items.length} kết quả cho "${keyword}"`);
                    } else {
                        Toast.warning(`Không tìm thấy kết quả nào cho "${keyword}"`);
                    }
                })
                .catch(error => {
                    console.error('Lỗi:', error);
                    resultContainer.innerHTML = `
                        <div class="alert alert-danger">
                            <i class="bi bi-exclamation-triangle-fill me-2"></i>
                            Đã xảy ra lỗi khi tải dữ liệu. Vui lòng thử lại.
                        </div>
                    `;
                    
                    // Hiển thị thông báo lỗi
                    Toast.error("Đã xảy ra lỗi khi tìm kiếm. Vui lòng thử lại.");
                });
        });
    });
}

// Hàm scroll đến kết quả tìm kiếm
function scrollToResults() {
    const resultsElement = document.getElementById('search-results');
    if (resultsElement) {
        // Tìm tiêu đề kết quả tìm kiếm nếu có
        const headerElement = resultsElement.querySelector('h2, h3, h4, .search-header');
        const targetElement = headerElement || resultsElement;
        
        // Lấy vị trí của phần tử mục tiêu
        const elementPosition = targetElement.getBoundingClientRect().top;
        
        // Tính toán vị trí scroll, trừ đi 120px để đảm bảo tiêu đề hiển thị đầy đủ
        const offsetPosition = elementPosition + window.scrollY - 120;
        
        // Scroll đến vị trí đó với hiệu ứng mượt
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}

// Thiết lập pagination AJAX
function setupPagination() {
    // Delegate event cho các pagination links
    document.getElementById('search-results')?.addEventListener('click', function(e) {
        const paginationLink = e.target.closest('.pagination a');
        if (!paginationLink) return;
        
        e.preventDefault();
        const resultContainer = document.getElementById('search-results');
        
        // Hiển thị trạng thái loading
        resultContainer.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Đang tải...</span>
                </div>
                <p class="mt-3">Đang tải trang...</p>
            </div>
        `;
        
        // URL cho fetch và history là giống nhau
        const url = paginationLink.href;
        
        // Update browser history
        window.history.pushState({}, '', url);
        
        // Scroll to search results
        scrollToResults();
        
        // Fetch nội dung
        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                if (!response.ok) throw new Error('Lỗi khi tải dữ liệu');
                return response.text();
            })
            .then(html => {
                // Cập nhật nội dung
                resultContainer.innerHTML = html;
                
                // Khởi tạo lại các sự kiện sau khi nội dung được cập nhật
                setupWishlistButtons();
                
                // Scroll to the top of results
                scrollToResults();
            })
            .catch(error => {
                console.error('Lỗi:', error);
                resultContainer.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="bi bi-exclamation-triangle-fill me-2"></i>
                        Đã xảy ra lỗi khi tải dữ liệu. Vui lòng thử lại.
                    </div>
                `;
            });
    });
}

// Thiết lập hero search form
function setupHeroSearchForm() {
    const heroForm = document.getElementById('hero-search-form');
    if (!heroForm) return;
    
    heroForm.addEventListener('submit', function(e) {
        const keywordInput = this.querySelector('input[name="keyword"]');
        const keyword = keywordInput?.value?.trim();
        
        if (!keyword) {
            e.preventDefault();
            
            // Hiển thị toast thông báo
            Toast.error("Vui lòng nhập từ khóa tìm kiếm", "Lỗi tìm kiếm");
            
            // Hiệu ứng rung cho input
            keywordInput.classList.add('shake-x');
            setTimeout(() => {
                keywordInput.classList.remove('shake-x');
            }, 1000);
            
            // Focus vào input
            keywordInput.focus();
        } else {
            // Nếu form hợp lệ, thêm sự kiện scroll sau khi trang tải xong
            localStorage.setItem('scrollToResults', 'true');
        }
    });
    
    // Kiểm tra nếu cần scroll sau khi trang tải xong
    if (localStorage.getItem('scrollToResults') === 'true') {
        // Xóa flag
        localStorage.removeItem('scrollToResults');
        
        // Scroll đến kết quả sau một khoảng thời gian ngắn để đảm bảo trang đã tải xong
        setTimeout(() => {
            scrollToResults();
        }, 500);
    }
}

// Kiểm tra và scroll đến kết quả nếu cần
function checkAndScrollToResults() {
    // Kiểm tra nếu có tham số URL là keyword hoặc page > 1, thì scroll đến kết quả
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('keyword') || (urlParams.has('page') && urlParams.get('page') > 1)) {
        // Scroll sau một khoảng thời gian ngắn để đảm bảo trang đã tải xong
        setTimeout(() => {
            scrollToResults();
        }, 300);
    }
}
