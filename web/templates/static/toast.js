/**
 * Toast Notification System
 * 
 * This file contains functions for displaying toast notifications.
 */

// Core showToast function that other functions will use
window.showToast = function(message, title = "Thông báo", type = "info") {
    const toastEl = document.getElementById('liveToast');
    if (!toastEl) {
        console.warn("Toast element not found");
        return;
    }
    
    // Set toast content
    document.getElementById('toastMessage').textContent = message;
    document.getElementById('toastTitle').textContent = title;
    document.getElementById('toastTime').textContent = "Vừa xong";
    
    // Set icon and color based on type
    const iconEl = document.getElementById('toastIcon');
    iconEl.className = "bi me-2 ";
    
    // Remove any previous background classes
    toastEl.classList.remove('bg-primary', 'bg-success', 'bg-warning', 'bg-danger', 'bg-info');
    toastEl.classList.remove('text-white', 'text-dark');
    
    switch(type) {
        case "success":
            iconEl.className += "bi-check-circle-fill text-white";
            toastEl.classList.add('bg-success', 'text-white');
            break;
        case "warning":
            iconEl.className += "bi-exclamation-triangle-fill text-dark";
            toastEl.classList.add('bg-warning', 'text-dark');
            break;
        case "error":
            iconEl.className += "bi-x-circle-fill text-white";
            toastEl.classList.add('bg-danger', 'text-white');
            break;
        case "info":
        default:
            iconEl.className += "bi-info-circle text-white";
            toastEl.classList.add('bg-primary', 'text-white');
            break;
    }
    
    // Show the toast
    if (window.toastInstance) {
        window.toastInstance.show();
    } else {
        console.warn("Toast instance not initialized");
    }
};

// Toast helper object with shorthand methods
const Toast = {
    /**
     * Show a toast notification
     * 
     * @param {string} message - The message to display
     * @param {string} title - The title of the toast (optional)
     * @param {string} type - The type of toast: 'info', 'success', 'warning', 'error' (optional)
     */
    show: function(message, title = "Thông báo", type = "info") {
        window.showToast(message, title, type);
    },
    
    /**
     * Show an info toast notification
     * 
     * @param {string} message - The message to display
     * @param {string} title - The title of the toast (optional)
     */
    info: function(message, title = "Thông tin") {
        this.show(message, title, "info");
    },
    
    /**
     * Show a success toast notification
     * 
     * @param {string} message - The message to display
     * @param {string} title - The title of the toast (optional)
     */
    success: function(message, title = "Thành công") {
        this.show(message, title, "success");
    },
    
    /**
     * Show a warning toast notification
     * 
     * @param {string} message - The message to display
     * @param {string} title - The title of the toast (optional)
     */
    warning: function(message, title = "Cảnh báo") {
        this.show(message, title, "warning");
    },
    
    /**
     * Show an error toast notification
     * 
     * @param {string} message - The message to display
     * @param {string} title - The title of the toast (optional)
     */
    error: function(message, title = "Lỗi") {
        this.show(message, title, "error");
    }
};

// Initialize toast-related events when the DOM is ready
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