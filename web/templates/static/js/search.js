/**
 * Search Functionality
 * Xử lý form tìm kiếm và hiển thị kết quả
 */

document.addEventListener('DOMContentLoaded', function() {
    // Kích hoạt xử lý tìm kiếm bằng JavaScript
    window.handleSearchWithJS = true;
    
    // Thiết lập form tìm kiếm với AJAX
    setupSearchForm();
    
    // Thiết lập các tính năng tìm kiếm nâng cao
    setupEnhancedSearch();
});

/**
 * Thiết lập form tìm kiếm với AJAX
 */
function setupSearchForm() {
    const searchForms = document.querySelectorAll('form[action="/search"]');
    if (searchForms.length === 0) return;
    
    searchForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Luôn ngăn hành vi mặc định để xử lý bằng JS
            e.preventDefault();
            
            const keywordInput = this.querySelector('input[name="keyword"]');
            const keyword = keywordInput?.value?.trim();
            
            if (!keyword) {
                // Hiển thị thông báo lỗi với Toast
                if (typeof Toast !== 'undefined') {
                    Toast.error("Vui lòng nhập từ khóa tìm kiếm", "Lỗi tìm kiếm");
                } else {
                    alert("Vui lòng nhập từ khóa tìm kiếm");
                }
                
                // Hiệu ứng rung cho input
                keywordInput.classList.add('shake-x');
                setTimeout(() => {
                    keywordInput.classList.remove('shake-x');
                }, 1000);
                
                keywordInput.focus();
                return;
            }
            
            const searchType = this.querySelector('select[name="search_type"]')?.value || 'title';
            const resultContainer = document.getElementById('search-results');
            
            if (!resultContainer) {
                // Nếu không có container kết quả, chuyển hướng thay vì AJAX
                const searchUrl = `/search?keyword=${encodeURIComponent(keyword)}&search_type=${searchType}`;
                window.location.href = searchUrl;
                return;
            }
            
            // Hiển thị trạng thái đang tải
            displayLoadingIndicator(resultContainer);
            
            // Lưu vào lịch sử tìm kiếm
            saveSearchHistory(keyword);
            
            // Tạo URL và cập nhật lịch sử
            const params = new URLSearchParams({
                keyword: keyword,
                search_type: searchType
            });
            
            const fetchUrl = `/search?${params.toString()}`;
            
            // Cập nhật URL trong trình duyệt không làm tải lại trang
            window.history.pushState({keyword, searchType}, '', fetchUrl);
            
            // Đóng dropdown nếu đang mở
            const searchDropdown = document.getElementById('search-suggestions');
            if (searchDropdown && searchDropdown.classList.contains('active')) {
                searchDropdown.classList.remove('active');
            }
            
            // Lấy kết quả
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
                    if (typeof setupWishlistButtons === 'function') {
                        setupWishlistButtons();
                    }
                    
                    // Cuộn đến đầu kết quả sau khi nội dung được cập nhật
                    setTimeout(() => {
                        scrollToResults();
                    }, 100);
                    
                    // Hiển thị thông báo thành công nếu có kết quả
                    const items = resultContainer.querySelectorAll('.book-card');
                    if (typeof Toast !== 'undefined') {
                        if (items.length > 0) {
                            Toast.success(`Đã tìm thấy ${items.length} kết quả cho "${keyword}"`);
                        } else {
                            Toast.warning(`Không tìm thấy kết quả nào cho "${keyword}"`);
                        }
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    resultContainer.innerHTML = `
                        <div class="alert alert-danger">
                            <i class="bi bi-exclamation-triangle-fill me-2"></i>
                            Đã xảy ra lỗi khi tải dữ liệu. Vui lòng thử lại.
                        </div>
                    `;
                    
                    // Hiển thị thông báo lỗi
                    if (typeof Toast !== 'undefined') {
                        Toast.error("Đã xảy ra lỗi khi tìm kiếm. Vui lòng thử lại.");
                    }
                });
        });
    });
    
    // Bắt sự kiện popstate (khi người dùng nhấn nút Back/Forward)
    window.addEventListener('popstate', function(event) {
        const searchResultsContainer = document.getElementById('search-results');
        if (searchResultsContainer) {
            // Lấy thông tin từ URL hiện tại
            const urlParams = new URLSearchParams(window.location.search);
            const keyword = urlParams.get('keyword');
            const searchType = urlParams.get('search_type') || 'title';
            
            if (keyword) {
                // Cập nhật input tìm kiếm
                const searchInput = document.getElementById('header-search-input');
                if (searchInput) {
                    searchInput.value = keyword;
                    toggleClearButton(searchInput);
                }
                
                // Hiển thị trạng thái đang tải
                displayLoadingIndicator(searchResultsContainer);
                
                // Lấy kết quả
                fetch(window.location.href, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.text())
                .then(html => {
                    searchResultsContainer.innerHTML = html;
                    
                    // Khởi tạo lại các sự kiện sau khi nội dung được cập nhật
                    if (typeof setupWishlistButtons === 'function') {
                        setupWishlistButtons();
                    }
                    
                    // Cuộn đến kết quả
                    scrollToResults();
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        }
    });
    
    // Xử lý xóa nội dung tìm kiếm
    setupSearchInputClearing();
}

/**
 * Thiết lập tính năng tìm kiếm nâng cao
 */
function setupEnhancedSearch() {
    const searchInput = document.getElementById('header-search-input');
    const searchDropdown = document.getElementById('search-suggestions');
    const searchHistoryContainer = document.getElementById('search-history-items');
    
    if (!searchInput || !searchDropdown || !searchHistoryContainer) return;
    
    // Hiển thị lịch sử khi focus vào input
    searchInput.addEventListener('focus', function() {
        searchDropdown.classList.add('active');
        displaySearchHistory();
    });
    
    // Ẩn dropdown khi click bên ngoài
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
            searchDropdown.classList.remove('active');
        }
    });
    
    // Xử lý khi click vào mục lịch sử
    searchDropdown.addEventListener('click', function(e) {
        const historyItem = e.target.closest('.dropdown-item');
        if (historyItem) {
            const text = historyItem.textContent.trim();
            // Trích xuất từ khóa tìm kiếm không có icon
            const searchTerm = text.replace(/^[\u2000-\u2FFF\u3000-\u9FFF\uF900-\uFDFF\uFE70-\uFEFF]/, '').trim();
            searchInput.value = searchTerm;
            searchDropdown.classList.remove('active');
            
            // Submit form tìm kiếm
            document.getElementById('header-search-form').dispatchEvent(new Event('submit'));
        }
    });
    
    // Xử lý khi gõ vào ô tìm kiếm
    let debounceTimer;
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.trim();
        
        // Xóa bộ hẹn giờ trước đó
        clearTimeout(debounceTimer);
        
        // Đặt bộ hẹn giờ mới để debounce
        debounceTimer = setTimeout(() => {
            if (searchTerm.length === 0) {
                displaySearchHistory();
            }
        }, 300);
        
        // Hiển thị/ẩn nút xóa
        toggleClearButton(this);
    });
}

/**
 * Hiển thị chỉ báo đang tải trong kết quả tìm kiếm
 */
function displayLoadingIndicator(container) {
    if (container) {
        container.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Đang tìm kiếm...</span>
                </div>
                <p class="mt-3">Đang tìm kiếm...</p>
            </div>
        `;
    }
}

/**
 * Thiết lập chức năng xóa nội dung tìm kiếm
 */
function setupSearchInputClearing() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(searchInput => {
        if (!searchInput) return;
        
        // Thêm chức năng nút xóa
        const clearButton = searchInput.parentElement.querySelector('.search-clear');
        if (clearButton) {
            clearButton.addEventListener('click', function() {
                searchInput.value = '';
                searchInput.focus();
                toggleClearButton(searchInput);
                
                // Nếu ở chế độ dropdown, hiển thị lịch sử tìm kiếm
                if (searchInput.id === 'header-search-input') {
                    displaySearchHistory();
                }
            });
        }
        
        // Trạng thái ban đầu cho nút xóa
        toggleClearButton(searchInput);
    });
}

/**
 * Bật/tắt hiển thị nút xóa
 */
function toggleClearButton(input) {
    const clearButton = input.parentElement.querySelector('.search-clear');
    if (clearButton) {
        clearButton.style.display = input.value.length > 0 ? 'block' : 'none';
    }
}

/**
 * Lưu tìm kiếm vào lịch sử
 */
function saveSearchHistory(term) {
    if (!term) return;
    
    let history = JSON.parse(localStorage.getItem('searchHistory')) || [];
    
    // Xóa nếu đã tồn tại (để chuyển lên đầu)
    history = history.filter(item => item.toLowerCase() !== term.toLowerCase());
    
    // Thêm vào đầu
    history.unshift(term);
    
    // Giới hạn 5 mục
    if (history.length > 5) {
        history = history.slice(0, 5);
    }
    
    // Lưu trở lại localStorage
    localStorage.setItem('searchHistory', JSON.stringify(history));
}

/**
 * Hiển thị lịch sử tìm kiếm
 */
function displaySearchHistory() {
    const historyContainer = document.getElementById('search-history-items');
    if (!historyContainer) return;
    
    const history = JSON.parse(localStorage.getItem('searchHistory')) || [];
    
    // Xóa container
    historyContainer.innerHTML = '';
    
    // Thêm các mục lịch sử
    if (history.length === 0) {
        historyContainer.innerHTML = '<p class="text-muted small px-3 py-2">Chưa có lịch sử tìm kiếm</p>';
    } else {
        history.forEach(term => {
            const historyItem = document.createElement('a');
            historyItem.className = 'dropdown-item history-item';
            historyItem.href = '#';
            historyItem.innerHTML = `<i class="bi bi-clock-history me-2"></i>${term}`;
            historyContainer.appendChild(historyItem);
        });
    }
    
    // Hiển thị dropdown
    const dropdown = document.getElementById('search-suggestions');
    if (dropdown) {
        dropdown.classList.add('active');
    }
}

/**
 * Cuộn đến kết quả tìm kiếm
 */
function scrollToResults() {
    const resultsContainer = document.getElementById('search-results');
    if (resultsContainer) {
        resultsContainer.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start'
        });
    }
} 