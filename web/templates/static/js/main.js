/**
 * Main JavaScript File
 * Minimal clean version with only essential functionality
 */

document.addEventListener('DOMContentLoaded', initApp);

/**
 * Main initialization function
 */
function initApp() {
    // Core functionality
    initTooltips();
    setupBackToTop();
    setupHeaderScroll();
    
    // Page-specific functionality
    setupBookCards();
    setupBookDetailsPage();
    setupSearchFunctionality();
}

// ==========================================
// CORE UI FUNCTIONALITY
// ==========================================

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0 && typeof bootstrap !== 'undefined') {
        [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
}

/**
 * Setup back to top button
 */
function setupBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');
    if (!backToTopBtn) return;
    
    window.addEventListener('scroll', function() {
        backToTopBtn.classList.toggle('show', window.pageYOffset > 300);
    });
    
    backToTopBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * Setup header scroll behavior
 */
function setupHeaderScroll() {
    const header = document.querySelector('.main-header');
    if (!header) return;
    
    let lastScroll = 0;
    const scrollThreshold = 50; // Ngưỡng scroll để kích hoạt hiệu ứng
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        // Thêm class khi scroll xuống
        if (currentScroll > scrollThreshold) {
            header.classList.add('header-scrolled');
        } else {
            header.classList.remove('header-scrolled');
        }
        
        // Ẩn/hiện header dựa trên hướng scroll
        if (currentScroll > lastScroll && currentScroll > 100) {
            // Scroll xuống
            header.classList.add('header-hidden');
        } else {
            // Scroll lên
            header.classList.remove('header-hidden');
        }
        
        lastScroll = currentScroll;
    });
}

// ==========================================
// BOOK FUNCTIONALITY
// ==========================================

/**
 * Setup all book card related functionality
 */
function setupBookCards() {
    setupClickableBookCards();
}

/**
 * Make book cards clickable
 */
function setupClickableBookCards() {
    const bookCards = document.querySelectorAll('.book-card');
    if (!bookCards.length) return;
    
    bookCards.forEach(card => {
        const titleLink = card.querySelector('.book-title a');
        if (!titleLink) return;
        
        const detailUrl = titleLink.getAttribute('href');
        
        card.addEventListener('click', function(e) {
            // Don't trigger if clicking on an interactive element
            if (e.target.closest('a, button')) {
                return;
            }
            
            window.location.href = detailUrl;
        });
    });
}

/**
 * Setup book details page
 */
function setupBookDetailsPage() {
    if (!document.querySelector('.book-details-container')) return;
    setupDescriptionToggle();
}

/**
 * Toggle description expand/collapse
 */
function setupDescriptionToggle() {
    const toggleBtn = document.querySelector('.toggle-description');
    if (!toggleBtn) return;
    
    toggleBtn.addEventListener('click', function() {
        const preview = document.querySelector('.description-preview');
        const full = document.querySelector('.description-full');
        const showMore = document.querySelector('.show-more');
        const showLess = document.querySelector('.show-less');
        
        if (preview) preview.classList.toggle('d-none');
        if (full) full.classList.toggle('d-none');
        if (showMore) showMore.classList.toggle('d-none');
        if (showLess) showLess.classList.toggle('d-none');
    });
}

// ==========================================
// SEARCH FUNCTIONALITY
// ==========================================

/**
 * Setup search related functionality
 */
function setupSearchFunctionality() {
    setupHeroSearchForm();
    setupPagination();
}

/**
 * Setup hero search form validation
 */
function setupHeroSearchForm() {
    const heroForm = document.getElementById('hero-search-form');
    if (!heroForm) return;
    
    heroForm.addEventListener('submit', function(e) {
        const keywordInput = this.querySelector('input[name="keyword"]');
        const keyword = keywordInput?.value?.trim();
        
        if (!keyword) {
            e.preventDefault();
            showErrorToast("Vui lòng nhập từ khóa tìm kiếm");
            keywordInput.focus();
        }
    });
}

/**
 * Setup pagination with AJAX
 */
function setupPagination() {
    const searchResults = document.getElementById('search-results');
    if (!searchResults) return;
    
    let isLoading = false;
    
    searchResults.addEventListener('click', async function(e) {
        const paginationLink = e.target.closest('.pagination a');
        if (!paginationLink || isLoading) return;
        
        e.preventDefault();
        
        // Prevent multiple clicks while loading
        isLoading = true;
        
        // Show loading state
        const originalContent = searchResults.innerHTML;
        searchResults.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Đang tải...</span>
                </div>
                <p class="mt-3">Đang tải trang...</p>
            </div>
        `;
        
        try {
            // Update URL
            const url = paginationLink.href;
            window.history.pushState({}, '', url);
            
            // Fetch content
            const response = await fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const html = await response.text();
            searchResults.innerHTML = html;
            
            // Reinitialize book card events for the new content
            setupBookCards();
            
            // Scroll to top of results
            searchResults.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
        } catch (error) {
            console.error('Lỗi:', error);
            searchResults.innerHTML = `
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    Đã xảy ra lỗi khi tải dữ liệu. Vui lòng thử lại.
                </div>
            `;
            showErrorToast("Đã xảy ra lỗi khi tải trang. Vui lòng thử lại.");
            
            // Restore original content after a delay
            setTimeout(() => {
                searchResults.innerHTML = originalContent;
                // Reinitialize book card events for restored content
                setupBookCards();
            }, 3000);
        } finally {
            isLoading = false;
        }
    });
}

// ==========================================
// TOAST NOTIFICATIONS
// ==========================================

/**
 * Show a toast notification
 */
function showToast(message, type = "info") {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Close notification when clicking the close button
    notification.querySelector('.notification-close').addEventListener('click', function() {
        document.body.removeChild(notification);
    });
    
    // Auto-remove notification after 5 seconds
    setTimeout(() => {
        if (document.body.contains(notification)) {
            document.body.removeChild(notification);
        }
    }, 1000);
}

/**
 * Show an error toast
 */
function showErrorToast(message) {
    showToast(message, "error");
}

/**
 * Show a success toast
 */
function showSuccessToast(message) {
    showToast(message, "success");
}

// Check for error parameters on page load
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('error')) {
        setTimeout(() => {
            showErrorToast(decodeURIComponent(urlParams.get('error')));
        }, 300);
    }
    
    const alertError = document.querySelector('.alert-danger');
    if (alertError) {
        setTimeout(() => {
            showErrorToast(alertError.textContent.trim());
        }, 300);
    }
}); 