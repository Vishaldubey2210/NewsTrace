/**
 * NewsTrace Search Page JavaScript - ENHANCED VERSION
 * Handles autonomous profiling workflow with loading and toasts
 * Version: 2.0
 */

$(document).ready(function() {
    console.log('Search page loaded');
    
    // Search form submission
    $('#searchForm').on('submit', function(e) {
        e.preventDefault();
        
        const outletName = $('#outletName').val().trim();
        
        if (!outletName) {
            showToast('Please enter a news outlet name', 'warning');
            return;
        }
        
        console.log('Starting profiling for:', outletName);
        startProfiling(outletName);
    });
    
    // Load recent jobs on page load
    loadRecentJobs();
});

// ==================== MAIN PROFILING FUNCTION ====================

/**
 * Start autonomous profiling workflow
 */
function startProfiling(outletName) {
    console.log('[START] Profiling:', outletName);
    
    // Hide previous states
    $('#resultsPreview').hide();
    $('#errorState').hide();
    
    // Show loading overlay with custom message
    showLoading(
        'Autonomous Profiling in Progress...',
        `Detecting website and extracting profiles for ${outletName}`
    );
    
    // Set button loading state
    setButtonLoading('#submitBtn', true);
    
    // Simulate progress steps (visual feedback)
    simulateProgress();
    
    // API call to start profiling
    $.ajax({
        url: '/api/profile',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ outlet_name: outletName }),
        timeout: 120000, // 2 minutes timeout
        success: function(response) {
            console.log('[SUCCESS] API Response:', response);
            hideLoading();
            setButtonLoading('#submitBtn', false);
            handleSuccess(response);
        },
        error: function(xhr, status, error) {
            console.error('[ERROR] API Failed:', status, error);
            console.error('Response:', xhr.responseText);
            
            hideLoading();
            setButtonLoading('#submitBtn', false);
            
            let errorData = { error: 'Unknown error occurred' };
            try {
                errorData = xhr.responseJSON || errorData;
            } catch (e) {
                errorData.error = xhr.responseText || error || 'Network error';
            }
            
            handleError(errorData);
        }
    });
}

// ==================== PROGRESS SIMULATION ====================

/**
 * Simulate progress steps for visual feedback
 */
function simulateProgress() {
    // If you have step indicators in HTML
    const steps = [
        { selector: '#step1', text: 'Detecting official website...', delay: 1000 },
        { selector: '#step2', text: 'Extracting journalist profiles...', delay: 3000 },
        { selector: '#step3', text: 'Processing and analyzing data...', delay: 5000 }
    ];
    
    steps.forEach((step, index) => {
        setTimeout(() => {
            // Update step indicator if exists
            if ($(step.selector).length) {
                $(step.selector).addClass('active');
                
                // Mark previous as completed
                if (index > 0 && $(steps[index - 1].selector).length) {
                    $(steps[index - 1].selector).removeClass('active').addClass('completed');
                }
            }
            
            // Update status text if exists
            if ($('#statusText').length) {
                $('#statusText').text(step.text);
            }
        }, step.delay);
    });
}

// ==================== SUCCESS HANDLER ====================

/**
 * Handle successful profiling
 */
function handleSuccess(response) {
    console.log('[HANDLE SUCCESS]', response);
    
    if (response.success) {
        const profileCount = response.profile_count || 0;
        const outletId = response.outlet_id || 1;
        const outletName = response.outlet_name || 'Unknown';
        
        // Show success toast
        showToast(
            `Successfully profiled ${profileCount} journalists from ${outletName}!`,
            'success',
            6000
        );
        
        // Update results preview
        if ($('#profileCount').length) {
            $('#profileCount').text(profileCount);
        }
        
        if ($('#viewResultsBtn').length) {
            $('#viewResultsBtn').attr('href', '/results/' + outletId);
        }
        
        if ($('#resultsPreview').length) {
            $('#resultsPreview').fadeIn();
        }
        
        // Add to recent searches
        addToRecentSearches(outletName, profileCount);
        
        // Reload recent jobs
        setTimeout(() => {
            loadRecentJobs();
        }, 1000);
        
    } else {
        handleError(response);
    }
}

// ==================== ERROR HANDLER ====================

/**
 * Handle profiling error
 */
function handleError(error) {
    console.log('[HANDLE ERROR]', error);
    
    const errorMsg = error.error || 'An unexpected error occurred';
    
    // Show error toast
    showToast(errorMsg, 'error', 7000);
    
    // Update error state in UI if exists
    if ($('#errorMessage').length) {
        $('#errorMessage').text(errorMsg);
    }
    
    if ($('#errorState').length) {
        $('#errorState').fadeIn();
    }
    
    // Provide helpful tips based on error
    if (errorMsg.includes('Website detection failed')) {
        showToast('Try using full outlet name (e.g., "The Hindu" instead of "Hindu")', 'info', 5000);
    } else if (errorMsg.includes('timeout')) {
        showToast('Request timed out. The outlet might have strong anti-scraping measures.', 'warning', 5000);
    }
}

// ==================== RECENT SEARCHES ====================

/**
 * Add to recent searches (client-side display)
 */
function addToRecentSearches(outletName, count) {
    const recentDiv = $('#recentSearches');
    
    if (recentDiv.length === 0) {
        return;
    }
    
    const timestamp = new Date().toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    const item = `
        <div class="d-flex justify-content-between align-items-center mb-2 p-2" 
             style="background: rgba(255,255,255,0.05); border-radius: 8px; animation: slideIn 0.3s ease-out;">
            <div>
                <strong>${outletName}</strong>
                <small class="d-block text-muted">
                    <i class="fas fa-clock me-1"></i>${timestamp}
                </small>
            </div>
            <span class="badge bg-primary">
                <i class="fas fa-users me-1"></i>${count} profiles
            </span>
        </div>
    `;
    
    recentDiv.prepend(item);
    
    // Limit to 5 recent searches
    if (recentDiv.children().length > 5) {
        recentDiv.children().last().remove();
    }
}

// ==================== RECENT JOBS ====================

/**
 * Load recent jobs from API
 */
function loadRecentJobs() {
    console.log('[LOADING] Recent jobs...');
    
    $.ajax({
        url: '/api/jobs/recent?limit=5',
        method: 'GET',
        success: function(response) {
            console.log('[JOBS]', response);
            if (response.success && response.jobs && response.jobs.length > 0) {
                displayRecentJobs(response.jobs);
            } else {
                displayEmptyJobs();
            }
        },
        error: function(xhr, status, error) {
            console.error('[ERROR] Loading jobs failed:', error);
            displayEmptyJobs();
        }
    });
}

/**
 * Display recent jobs in UI
 */
function displayRecentJobs(jobs) {
    const recentDiv = $('#recentSearches');
    
    if (recentDiv.length === 0) {
        return;
    }
    
    recentDiv.empty();
    
    jobs.forEach(job => {
        const statusClass = getStatusClass(job.status);
        const statusIcon = getStatusIcon(job.status);
        const profileCount = job.profiles_found || 0;
        
        const item = `
            <div class="d-flex justify-content-between align-items-center mb-2 p-2" 
                 style="background: rgba(255,255,255,0.05); border-radius: 8px;">
                <div>
                    <strong>${job.outlet_name}</strong>
                    <small class="d-block text-muted">
                        <i class="fas fa-clock me-1"></i>${formatDate(job.started_at)}
                    </small>
                </div>
                <span class="badge bg-${statusClass}">
                    <i class="fas ${statusIcon} me-1"></i>${profileCount} profiles
                </span>
            </div>
        `;
        
        recentDiv.append(item);
    });
}

/**
 * Display empty state for recent jobs
 */
function displayEmptyJobs() {
    const recentDiv = $('#recentSearches');
    
    if (recentDiv.length === 0) {
        return;
    }
    
    recentDiv.html(`
        <div class="text-center text-muted p-4">
            <i class="fas fa-inbox fa-2x mb-3"></i>
            <p>No recent searches yet</p>
            <small>Start profiling a news outlet to see results here</small>
        </div>
    `);
}

// ==================== HELPER FUNCTIONS ====================

/**
 * Get Bootstrap class for job status
 */
function getStatusClass(status) {
    const statusMap = {
        'completed': 'success',
        'failed': 'danger',
        'running': 'warning',
        'pending': 'secondary'
    };
    return statusMap[status] || 'secondary';
}

/**
 * Get icon for job status
 */
function getStatusIcon(status) {
    const iconMap = {
        'completed': 'fa-check-circle',
        'failed': 'fa-times-circle',
        'running': 'fa-spinner fa-spin',
        'pending': 'fa-clock'
    };
    return iconMap[status] || 'fa-question-circle';
}

/**
 * Format date helper
 */
function formatDate(dateStr) {
    if (!dateStr) return 'Unknown';
    
    try {
        const date = new Date(dateStr);
        return date.toLocaleString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (e) {
        console.error('Date formatting error:', e);
        return dateStr;
    }
}

// ==================== EXPORT FUNCTIONALITY ====================

/**
 * Export CSV button handler
 */
$(document).on('click', '#exportCsvBtn', function(e) {
    e.preventDefault();
    
    const outletId = $(this).data('outlet-id') || 1;
    
    showToast('Preparing CSV export...', 'info', 2000);
    
    // Trigger download
    window.location.href = '/api/export/csv/' + outletId;
    
    setTimeout(() => {
        showToast('CSV export started!', 'success', 3000);
    }, 1000);
});

/**
 * Export JSON button handler
 */
$(document).on('click', '#exportJsonBtn', function(e) {
    e.preventDefault();
    
    const outletId = $(this).data('outlet-id') || 1;
    
    showToast('Preparing JSON export...', 'info', 2000);
    
    // Trigger download
    window.location.href = '/api/export/json/' + outletId;
    
    setTimeout(() => {
        showToast('JSON export started!', 'success', 3000);
    }, 1000);
});

// ==================== KEYBOARD SHORTCUTS ====================

/**
 * Handle Enter key on input field
 */
$('#outletName').on('keypress', function(e) {
    if (e.which === 13) { // Enter key
        e.preventDefault();
        $('#searchForm').submit();
    }
});

/**
 * Handle Ctrl+Enter for quick submit
 */
$(document).on('keydown', function(e) {
    if (e.ctrlKey && e.which === 13) {
        $('#searchForm').submit();
    }
});

// ==================== AUTO-SUGGESTIONS (Optional) ====================

/**
 * Popular Indian news outlets for auto-suggest
 */
const popularOutlets = [
    'The Hindu',
    'Indian Express',
    'Times of India',
    'Hindustan Times',
    'NDTV',
    'The Wire',
    'Scroll.in',
    'FirstPost',
    'The Quint',
    'News18'
];

/**
 * Setup auto-complete if needed
 */
function setupAutoComplete() {
    if ($('#outletName').length && typeof $.fn.autocomplete !== 'undefined') {
        $('#outletName').autocomplete({
            source: popularOutlets,
            minLength: 2
        });
    }
}

// Initialize auto-complete on page load
setupAutoComplete();

console.log('[LOADED] Search.js enhanced version loaded successfully');
