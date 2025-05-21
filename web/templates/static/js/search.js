/**
 * Search Functionality
 * This script handles the search form submission and results display
 */

document.addEventListener('DOMContentLoaded', function() {
    // Setup search form with AJAX
    setupSearchForm();
});

// Setup search form with AJAX
function setupSearchForm() {
    const searchForms = document.querySelectorAll('form[action="/search"]');
    if (searchForms.length === 0) return;
    
    searchForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Only prevent default if we're handling search with JS
            if (window.handleSearchWithJS) {
                e.preventDefault();
                
                const keywordInput = this.querySelector('input[name="keyword"]');
                const keyword = keywordInput?.value?.trim();
                
                if (!keyword) {
                    // Use toast notification instead of alert
                    Toast.error("Vui lòng nhập từ khóa tìm kiếm", "Lỗi tìm kiếm");
                    
                    // Add shake effect for input
                    keywordInput.classList.add('shake-x');
                    setTimeout(() => {
                        keywordInput.classList.remove('shake-x');
                    }, 1000);
                    
                    // Focus on input
                    keywordInput.focus();
                    return;
                }
                
                const searchType = this.querySelector('select[name="search_type"]')?.value || 'title';
                const resultContainer = document.getElementById('search-results');
                
                // Show loading state
                displayLoadingIndicator(resultContainer);
                
                // Create URL and update history
                const params = new URLSearchParams({
                    keyword: keyword,
                    search_type: searchType
                });
                
                const fetchUrl = `/search?${params.toString()}`;
                const historyUrl = fetchUrl; // Use same URL
                
                // Update URL in browser
                window.history.pushState({}, '', historyUrl);
                
                // Scroll to search results if function exists
                if (typeof scrollToResults === 'function') {
                    scrollToResults();
                }
                
                // Fetch results
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
                        // Update content
                        resultContainer.innerHTML = html;
                        
                        // Re-initialize events after content is updated
                        if (typeof setupWishlistButtons === 'function') {
                            setupWishlistButtons();
                        }
                        
                        // Scroll to the top of results
                        if (typeof scrollToResults === 'function') {
                            scrollToResults();
                        }
                        
                        // Show success notification if there are results
                        const items = resultContainer.querySelectorAll('.book-card');
                        if (items.length > 0) {
                            Toast.success(`Đã tìm thấy ${items.length} kết quả cho "${keyword}"`);
                        } else {
                            Toast.warning(`Không tìm thấy kết quả nào cho "${keyword}"`);
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
                        
                        // Show error notification
                        Toast.error("Đã xảy ra lỗi khi tìm kiếm. Vui lòng thử lại.");
                    });
            }
        });
    });
    
    // Handle search input clearing
    setupSearchInputClearing();
}

// Display loading indicator in search results
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

// Setup search input clearing functionality
function setupSearchInputClearing() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(searchInput => {
        if (!searchInput) return;
        
        // Add clear button functionality
        const clearButton = searchInput.parentElement.querySelector('.search-clear');
        if (clearButton) {
            clearButton.addEventListener('click', function() {
                searchInput.value = '';
                searchInput.focus();
                const searchResults = document.getElementById('search-results');
                if (searchResults) {
                    searchResults.innerHTML = '';
                }
            });
        }
        
        // Show/hide clear button based on input content
        searchInput.addEventListener('input', function() {
            if (clearButton) {
                clearButton.style.display = this.value.length > 0 ? 'block' : 'none';
            }
        });
        
        // Initial state for clear button
        if (clearButton && searchInput.value.length > 0) {
            clearButton.style.display = 'block';
        }
    });
} 