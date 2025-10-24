/**
 * NewsTrace Main JavaScript - ENHANCED VERSION
 * Global utilities with loading spinners and toast notifications
 * Version: 2.0
 */

// ==================== INITIALIZATION ====================

$(document).ready(function() {
    console.log('NewsTrace initialized');
    
    // Create toast container
    if ($('.toast-container').length === 0) {
        $('body').append('<div class="toast-container"></div>');
    }
    
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// ==================== GLOBAL VARIABLES ====================

const API_BASE_URL = window.location.origin;

// ==================== LOADING OVERLAY ====================

/**
 * Show full-screen loading overlay with spinner
 * @param {string} message - Main loading message
 * @param {string} subtext - Optional subtext
 */
function showLoading(message = 'Loading...', subtext = '') {
    // Remove existing loading overlay
    hideLoading();
    
    const overlay = `
        <div id="loadingOverlay" class="loading-overlay">
            <div class="spinner-container">
                <div class="spinner"></div>
                <div class="loading-text">${message}</div>
                ${subtext ? `<div class="loading-subtext">${subtext}</div>` : ''}
            </div>
        </div>
    `;
    
    $('body').append(overlay);
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    $('#loadingOverlay').fadeOut(300, function() {
        $(this).remove();
    });
}

// ==================== TOAST NOTIFICATIONS ====================

/**
 * Show toast notification
 * @param {string} message - Toast message
 * @param {string} type - Type: 'success', 'error', 'warning', 'info'
 * @param {number} duration - Auto-dismiss duration in ms (default: 5000)
 */
function showToast(message, type = 'info', duration = 5000) {
    const toastId = 'toast-' + Date.now();
    
    const toast = `
        <div id="${toastId}" class="toast-notification ${type}">
            <div>
                <strong>${getToastIcon(type)}</strong>
                <span>${message}</span>
            </div>
            <button class="toast-close" onclick="closeToast('${toastId}')">&times;</button>
        </div>
    `;
    
    $('.toast-container').append(toast);
    
    // Auto-remove after duration
    setTimeout(() => {
        closeToast(toastId);
    }, duration);
}

/**
 * Get icon for toast type
 * @param {string} type - Toast type
 * @returns {string} Icon text
 */
function getToastIcon(type) {
    const icons = {
        'success': '✓ Success!',
        'error': '✕ Error!',
        'warning': '⚠ Warning!',
        'info': 'ℹ Info'
    };
    return icons[type] || icons['info'];
}

/**
 * Close specific toast
 * @param {string} toastId - Toast element ID
 */
function closeToast(toastId) {
    $(`#${toastId}`).fadeOut(300, function() {
        $(this).remove();
    });
}

// ==================== BUTTON LOADING STATE ====================

/**
 * Set button loading state
 * @param {string} buttonSelector - jQuery selector for button
 * @param {boolean} loading - Loading state
 */
function setButtonLoading(buttonSelector, loading = true) {
    const $btn = $(buttonSelector);
    
    if (loading) {
        $btn.addClass('btn-loading');
        $btn.data('original-text', $btn.html());
        $btn.prop('disabled', true);
    } else {
        $btn.removeClass('btn-loading');
        const originalText = $btn.data('original-text');
        if (originalText) {
            $btn.html(originalText);
        }
        $btn.prop('disabled', false);
    }
}

// ==================== UTILITY FUNCTIONS ====================

/**
 * Format date to readable string
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    try {
        const date = new Date(dateString);
        return date.toLocaleString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (e) {
        console.error('Date formatting error:', e);
        return dateString;
    }
}

/**
 * Format number with commas
 * @param {number} num - Number to format
 * @returns {string} Formatted number
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Truncate text to specified length
 * @param {string} text - Text to truncate
 * @param {number} length - Max length
 * @returns {string} Truncated text
 */
function truncateText(text, length = 100) {
    if (!text) return '';
    return text.length > length ? text.substring(0, length) + '...' : text;
}

// ==================== AJAX ERROR HANDLING ====================

/**
 * Handle AJAX errors globally
 * @param {object} xhr - XMLHttpRequest object
 * @param {string} status - Error status
 * @param {string} error - Error message
 */
function handleAjaxError(xhr, status, error) {
    console.error('AJAX Error:', status, error);
    console.error('Response:', xhr.responseText);
    
    hideLoading();
    
    let errorMessage = 'An error occurred';
    
    try {
        if (xhr.responseJSON && xhr.responseJSON.error) {
            errorMessage = xhr.responseJSON.error;
        } else if (xhr.responseText) {
            errorMessage = xhr.responseText;
        } else if (error) {
            errorMessage = error;
        }
    } catch (e) {
        errorMessage = 'Network error occurred';
    }
    
    showToast(errorMessage, 'error', 7000);
}

// ==================== AJAX GLOBAL SETUP ====================

// Set up global AJAX handlers
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        console.log('[AJAX] Request:', settings.type, settings.url);
    },
    complete: function(xhr, status) {
        console.log('[AJAX] Complete:', status);
    }
});

// ==================== ELEMENT LOADING STATE ====================

/**
 * Show loading spinner inside element
 * @param {string} elementId - Element ID
 */
function showElementLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="text-center p-4"><div class="spinner"></div><p class="mt-3">Loading...</p></div>';
    }
}

/**
 * Hide element loading state
 * @param {string} elementId - Element ID
 */
function hideElementLoading(elementId) {
    // Implementation depends on what to show after loading
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

// ==================== VALIDATION HELPERS ====================

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} Is valid
 */
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validate URL format
 * @param {string} url - URL to validate
 * @returns {boolean} Is valid
 */
function isValidURL(url) {
    try {
        new URL(url);
        return true;
    } catch (e) {
        return false;
    }
}

// ==================== DEBOUNCE UTILITY ====================

/**
 * Debounce function execution
 * @param {function} func - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {function} Debounced function
 */
function debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ==================== CONFIRM DIALOG ====================

/**
 * Show confirmation dialog
 * @param {string} message - Confirmation message
 * @param {function} callback - Callback on confirm
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// ==================== COPY TO CLIPBOARD ====================

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!', 'success', 2000);
        }).catch(err => {
            console.error('Copy failed:', err);
            showToast('Failed to copy', 'error');
        });
    } else {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            showToast('Copied to clipboard!', 'success', 2000);
        } catch (err) {
            console.error('Copy failed:', err);
            showToast('Failed to copy', 'error');
        }
        document.body.removeChild(textarea);
    }
}

// ==================== SCROLL TO TOP ====================

/**
 * Smooth scroll to top of page
 */
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// ==================== EXPORTS (if using modules) ====================

// If you're using ES6 modules, uncomment below:
// export { showLoading, hideLoading, showToast, setButtonLoading, formatDate };

console.log('[LOADED] Main.js utilities loaded successfully');
