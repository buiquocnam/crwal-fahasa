/**
 * Main JavaScript File
 * This file initializes all the main functionality for the website
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    window.handleSearchWithJS = false; // Set to true to handle search with JS instead of form submission
    
    // Initialize tooltips
    initTooltips();
    
    // Mobile menu toggle
    setupMobileMenu();
    
    // Setup back to top button
    setupBackToTop();
    
    // Quantity controls for book details page
    setupQuantityControls();
    
    // Setup wishlist buttons
    setupWishlistButtons();

    // Setup description toggle
    setupDescriptionToggle();
    
    // Animated elements
    setupAnimatedElements();
    
    // Add to cart functionality
    setupAddToCart();
    
    // Handle theme switcher if present
    setupThemeSwitcher();

    // Setup pagination with AJAX
    setupPagination();

    // Setup hero search form
    setupHeroSearchForm();

    // Check and scroll to results if needed
    checkAndScrollToResults();
    
    // Make book cards clickable
    setupClickableBookCards();
    
    // Setup enhanced book details page
    setupBookDetailsPage();
});

// Initialize Bootstrap tooltips
function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (tooltipTriggerList.length > 0 && typeof bootstrap !== 'undefined') {
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Make book cards clickable
function setupClickableBookCards() {
    const bookCards = document.querySelectorAll('.book-card');
    
    bookCards.forEach(card => {
        // Get detail page URL from title link
        const titleLink = card.querySelector('.book-title a');
        if (!titleLink) return;
        
        const detailUrl = titleLink.getAttribute('href');
        
        // Make the entire card clickable
        card.addEventListener('click', function(e) {
            // Don't trigger if clicking on an interactive element (button, link)
            if (e.target.closest('.book-action-btn, a, button, .btn-wishlist')) {
                return;
            }
            
            // Add a subtle click effect
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
                // Navigate to the detail page
                window.location.href = detailUrl;
            }, 150);
        });
        
        // Add hover class to show it's clickable
        card.classList.add('clickable');
    });
}

// Enhanced setup for book details page
function setupBookDetailsPage() {
    // Check if we're on the book details page
    const bookDetailsContainer = document.querySelector('.book-details-container');
    if (!bookDetailsContainer) return;
    
    // Add hover animations to elements
    addHoverEffects();
    
    // Add image zoom interaction
    setupImageZoom();
    
    // Ensure animate.css classes are applied
    ensureAnimations();
}

// Add hover effects to elements
function addHoverEffects() {
    // Add subtle lift effect to badges
    document.querySelectorAll('.badge').forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
    
    // Add subtle hover effect to table rows
    document.querySelectorAll('.table tr').forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(var(--bs-primary-rgb), 0.05)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
}

// Setup image zoom on hover
function setupImageZoom() {
    const bookImage = document.querySelector('.book-details-image');
    if (!bookImage) return;
    
    const imageContainer = document.querySelector('.book-image-container');
    if (!imageContainer) return;
    
    // Original zoom effect is in CSS, but we can add extra interactions
    imageContainer.addEventListener('mousemove', function(e) {
        // Calculate mouse position
        const x = e.clientX - this.getBoundingClientRect().left;
        const y = e.clientY - this.getBoundingClientRect().top;
        
        // Calculate percentage position
        const xPercent = x / this.offsetWidth;
        const yPercent = y / this.offsetHeight;
        
        // Apply subtle transform to create a 3D effect
        bookImage.style.transformOrigin = `${xPercent * 100}% ${yPercent * 100}%`;
    });
    
    // Reset on mouse leave
    imageContainer.addEventListener('mouseleave', function() {
        bookImage.style.transformOrigin = 'center center';
    });
}

// Ensure animations are applied
function ensureAnimations() {
    // If animate.css classes don't work, apply manual animations
    setTimeout(() => {
        document.querySelectorAll('.animate__animated').forEach(element => {
            // Check if element is already animated
            const style = window.getComputedStyle(element);
            if (style.animationName === 'none') {
                // Apply manual animation
                element.style.opacity = '0';
                setTimeout(() => {
                    element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    element.style.opacity = '1';
                    
                    if (element.classList.contains('animate__fadeInUp')) {
                        element.style.transform = 'translateY(20px)';
                        setTimeout(() => {
                            element.style.transform = 'translateY(0)';
                        }, 50);
                    }
                    
                    if (element.classList.contains('animate__fadeInLeft')) {
                        element.style.transform = 'translateX(-20px)';
                        setTimeout(() => {
                            element.style.transform = 'translateX(0)';
                        }, 50);
                    }
                }, 100);
            }
        });
    }, 500);
}

// Setup mobile menu toggle
function setupMobileMenu() {
    const menuToggle = document.querySelector('.navbar-toggler');
    const mobileMenu = document.querySelector('.navbar-collapse');
    
    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('show');
            this.setAttribute('aria-expanded', 
                this.getAttribute('aria-expanded') === 'true' ? 'false' : 'true');
        });
    }
}

// Setup quantity controls for product detail page
function setupQuantityControls() {
    const quantityControls = document.querySelectorAll('.qty-btn');
    
    if (quantityControls.length > 0) {
        quantityControls.forEach(control => {
            control.addEventListener('click', function() {
                const input = this.parentElement.querySelector('.qty-input');
                let currentValue = parseInt(input.value);
                
                if (this.classList.contains('qty-decrease') && currentValue > 1) {
                    input.value = currentValue - 1;
                } else if (this.classList.contains('qty-increase')) {
                    input.value = currentValue + 1;
                }
            });
        });
    }
}

// Setup back to top button
function setupBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');
    
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
        
        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Setup wishlist buttons
function setupWishlistButtons() {
    document.querySelectorAll('.btn-wishlist').forEach(button => {
        button.addEventListener('click', toggleWishlist);
    });
}

// Toggle wishlist function
function toggleWishlist(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const icon = this.querySelector('i');
    if (icon) {
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
}

// Setup description toggle for book details
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
        
        // Add animation to the full description when showing
        if (!full.classList.contains('d-none')) {
            full.style.opacity = '0';
            full.style.transform = 'translateY(10px)';
            setTimeout(() => {
                full.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                full.style.opacity = '1';
                full.style.transform = 'translateY(0)';
            }, 50);
        }
    });
}

// Setup animated elements
function setupAnimatedElements() {
    const animatedElements = document.querySelectorAll('.animated');
    
    if (animatedElements.length > 0) {
        // Simple animation on scroll
        function checkIfInView() {
            animatedElements.forEach(element => {
                const rect = element.getBoundingClientRect();
                const windowHeight = window.innerHeight || document.documentElement.clientHeight;
                
                if (rect.top <= windowHeight * 0.8 && rect.bottom >= 0) {
                    element.classList.add('in-view');
                }
            });
        }
        
        // Initial check
        checkIfInView();
        
        // Check on scroll
        window.addEventListener('scroll', checkIfInView);
    }
}

// Setup add to cart functionality
function setupAddToCart() {
    const addToCartBtns = document.querySelectorAll('.add-to-cart');
    
    if (addToCartBtns.length > 0) {
        addToCartBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                
                const bookTitle = this.getAttribute('data-title') || 'Book';
                
                // Show notification
                Toast.success(`${bookTitle} has been added to your cart!`);
                
                // Update cart count (for demo purposes)
                const cartCount = document.querySelector('.cart-count');
                if (cartCount) {
                    let count = parseInt(cartCount.textContent);
                    cartCount.textContent = count + 1;
                    cartCount.classList.add('animate__animated', 'animate__heartBeat');
                    
                    setTimeout(() => {
                        cartCount.classList.remove('animate__animated', 'animate__heartBeat');
                    }, 1000);
                }
            });
        });
    }
}

// Setup theme switcher
function setupThemeSwitcher() {
    const themeSwitcher = document.querySelector('.theme-switch');
    
    if (themeSwitcher) {
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('theme');
        
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
            if (savedTheme === 'dark') {
                themeSwitcher.checked = true;
            }
        }
        
        themeSwitcher.addEventListener('change', function() {
            if (this.checked) {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        });
    }
}

// Setup pagination with AJAX
function setupPagination() {
    // Delegate event for pagination links
    document.getElementById('search-results')?.addEventListener('click', function(e) {
        const paginationLink = e.target.closest('.pagination a');
        if (!paginationLink) return;
        
        e.preventDefault();
        const resultContainer = document.getElementById('search-results');
        
        // Show loading state
        resultContainer.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Đang tải...</span>
                </div>
                <p class="mt-3">Đang tải trang...</p>
            </div>
        `;
        
        // URL for fetch and history
        const url = paginationLink.href;
        
        // Update browser history
        window.history.pushState({}, '', url);
        
        // Scroll to search results
        scrollToResults();
        
        // Fetch content
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
                // Update content
                resultContainer.innerHTML = html;
                
                // Re-initialize events after content update
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
                Toast.error("Đã xảy ra lỗi khi tải trang. Vui lòng thử lại.");
            });
    });
}

// Scroll to results function
function scrollToResults() {
    const resultsElement = document.getElementById('search-results');
    if (resultsElement) {
        // Find search results header if available
        const headerElement = resultsElement.querySelector('h2, h3, h4, .search-header');
        const targetElement = headerElement || resultsElement;
        
        // Get position of target element
        const elementPosition = targetElement.getBoundingClientRect().top;
        
        // Calculate scroll position, subtracting 120px for header space
        const offsetPosition = elementPosition + window.scrollY - 120;
        
        // Scroll to that position with smooth effect
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}

// Setup hero search form
function setupHeroSearchForm() {
    const heroForm = document.getElementById('hero-search-form');
    if (!heroForm) return;
    
    heroForm.addEventListener('submit', function(e) {
        const keywordInput = this.querySelector('input[name="keyword"]');
        const keyword = keywordInput?.value?.trim();
        
        if (!keyword) {
            e.preventDefault();
            
            // Display toast notification
            Toast.error("Vui lòng nhập từ khóa tìm kiếm", "Lỗi tìm kiếm");
            
            // Add shake effect for input
            keywordInput.classList.add('shake-x');
            setTimeout(() => {
                keywordInput.classList.remove('shake-x');
            }, 1000);
            
            // Focus on input
            keywordInput.focus();
        } else {
            // If form is valid, add scroll event after page loads
            localStorage.setItem('scrollToResults', 'true');
        }
    });
}

// Check and scroll to results if needed
function checkAndScrollToResults() {
    // Check if localStorage flag is set
    if (localStorage.getItem('scrollToResults') === 'true') {
        // Clear flag
        localStorage.removeItem('scrollToResults');
        
        // Scroll to results after a short delay to ensure page is loaded
        setTimeout(() => {
            scrollToResults();
        }, 500);
    }
    
    // Check if URL parameters include keyword or page > 1, then scroll to results
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('keyword') || (urlParams.has('page') && urlParams.get('page') > 1)) {
        // Scroll after a short delay to ensure page is loaded
        setTimeout(() => {
            scrollToResults();
        }, 300);
    }
}

/**
 * Toast Notification System
 */
window.showToast = function(message, title = "Thông báo", type = "info") {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} animate__animated animate__fadeInRight`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Close notification when clicking the close button
    notification.querySelector('.notification-close').addEventListener('click', function() {
        notification.classList.replace('animate__fadeInRight', 'animate__fadeOutRight');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
    
    // Auto-remove notification after 5 seconds
    setTimeout(() => {
        if (document.body.contains(notification)) {
            notification.classList.replace('animate__fadeInRight', 'animate__fadeOutRight');
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000);
};

// Toast helper object with shorthand methods
const Toast = {
    show: function(message, title = "Thông báo", type = "info") {
        window.showToast(message, title, type);
    },
    
    info: function(message, title = "Thông tin") {
        this.show(message, title, "info");
    },
    
    success: function(message, title = "Thành công") {
        this.show(message, title, "success");
    },
    
    warning: function(message, title = "Cảnh báo") {
        this.show(message, title, "warning");
    },
    
    error: function(message, title = "Lỗi") {
        this.show(message, title, "error");
    }
};

// Initialize toast-related events
document.addEventListener('DOMContentLoaded', function() {
    // Show toast if there's an error parameter in URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('error')) {
        setTimeout(() => {
            Toast.error(decodeURIComponent(urlParams.get('error')), "Lỗi");
        }, 300);
    }
    
    // If page has an error displayed in alert, also show it as toast
    const alertError = document.querySelector('.alert-danger');
    if (alertError) {
        setTimeout(() => {
            Toast.error(alertError.textContent.trim(), "Lỗi");
        }, 300);
    }
}); 