/**
 * NewsTrace API Utility Module
 * Centralized API calls with error handling
 * Version: 1.0
 */

const NewsTraceAPI = {
    baseURL: window.location.origin,
    
    // ==================== PROFILING ====================
    
    /**
     * Start profiling workflow for a news outlet
     * @param {string} outletName - Name of the outlet to profile
     * @returns {Promise} API response
     */
    profileOutlet: function(outletName) {
        return $.ajax({
            url: `${this.baseURL}/api/profile`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ outlet_name: outletName }),
            timeout: 120000
        });
    },
    
    // ==================== OUTLETS ====================
    
    /**
     * Get all registered outlets
     * @returns {Promise} API response
     */
    getOutlets: function() {
        return $.ajax({
            url: `${this.baseURL}/api/outlets`,
            method: 'GET'
        });
    },
    
    /**
     * Get single outlet by ID
     * @param {number} outletId - Outlet ID
     * @returns {Promise} API response
     */
    getOutlet: function(outletId) {
        return $.ajax({
            url: `${this.baseURL}/api/outlet/${outletId}`,
            method: 'GET'
        });
    },
    
    /**
     * Get journalists for an outlet
     * @param {number} outletId - Outlet ID
     * @returns {Promise} API response
     */
    getOutletJournalists: function(outletId) {
        return $.ajax({
            url: `${this.baseURL}/api/outlet/${outletId}/journalists`,
            method: 'GET'
        });
    },
    
    // ==================== JOBS ====================
    
    /**
     * Get recent scraping jobs
     * @param {number} limit - Number of jobs to fetch
     * @returns {Promise} API response
     */
    getRecentJobs: function(limit = 10) {
        return $.ajax({
            url: `${this.baseURL}/api/jobs/recent?limit=${limit}`,
            method: 'GET'
        });
    },
    
    /**
     * Get single job details
     * @param {number} jobId - Job ID
     * @returns {Promise} API response
     */
    getJob: function(jobId) {
        return $.ajax({
            url: `${this.baseURL}/api/jobs/${jobId}`,
            method: 'GET'
        });
    },
    
    // ==================== NETWORK GRAPH ====================
    
    /**
     * Get network graph data for visualization
     * @param {number} outletId - Outlet ID
     * @returns {Promise} API response
     */
    getNetworkGraph: function(outletId) {
        return $.ajax({
            url: `${this.baseURL}/api/network/graph/${outletId}`,
            method: 'GET'
        });
    },
    
    // ==================== ANALYTICS ====================
    
    /**
     * Get analytics statistics
     * @returns {Promise} API response
     */
    getAnalyticsStats: function() {
        return $.ajax({
            url: `${this.baseURL}/api/analytics/stats`,
            method: 'GET'
        });
    },
    
    /**
     * Get top journalists by influence score
     * @param {number} limit - Number of journalists
     * @returns {Promise} API response
     */
    getTopJournalists: function(limit = 10) {
        return $.ajax({
            url: `${this.baseURL}/api/journalists/top/${limit}`,
            method: 'GET'
        });
    },
    
    // ==================== EXPORT ====================
    
    /**
     * Export journalist data as CSV
     * @param {number} outletId - Outlet ID
     * @returns {string} Download URL
     */
    exportCSV: function(outletId) {
        return `${this.baseURL}/api/export/csv/${outletId}`;
    },
    
    /**
     * Export journalist data as JSON
     * @param {number} outletId - Outlet ID
     * @returns {string} Download URL
     */
    exportJSON: function(outletId) {
        return `${this.baseURL}/api/export/json/${outletId}`;
    },
    
    /**
     * Trigger CSV download
     * @param {number} outletId - Outlet ID
     */
    downloadCSV: function(outletId) {
        window.location.href = this.exportCSV(outletId);
    },
    
    /**
     * Trigger JSON download
     * @param {number} outletId - Outlet ID
     */
    downloadJSON: function(outletId) {
        window.location.href = this.exportJSON(outletId);
    },
    
    // ==================== UTILITY ====================
    
    /**
     * Health check endpoint
     * @returns {Promise} API response
     */
    healthCheck: function() {
        return $.ajax({
            url: `${this.baseURL}/api/health`,
            method: 'GET'
        });
    },
    
    /**
     * Test website detection
     * @param {string} outletName - Outlet name
     * @returns {Promise} API response
     */
    testWebsiteDetection: function(outletName) {
        return $.ajax({
            url: `${this.baseURL}/api/search/detect`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ outlet_name: outletName })
        });
    }
};

// ==================== WRAPPER FUNCTIONS WITH ERROR HANDLING ====================

/**
 * Safe API call with automatic error handling
 * @param {Promise} apiPromise - API promise
 * @param {Object} options - Options {showLoading, loadingMessage, successMessage}
 * @returns {Promise} Wrapped promise
 */
function safeAPICall(apiPromise, options = {}) {
    const defaults = {
        showLoading: false,
        loadingMessage: 'Loading...',
        successMessage: null,
        errorMessage: 'An error occurred'
    };
    
    const opts = { ...defaults, ...options };
    
    if (opts.showLoading) {
        showLoading(opts.loadingMessage);
    }
    
    return apiPromise
        .done(function(response) {
            if (opts.showLoading) {
                hideLoading();
            }
            
            if (opts.successMessage) {
                showToast(opts.successMessage, 'success');
            }
            
            return response;
        })
        .fail(function(xhr, status, error) {
            if (opts.showLoading) {
                hideLoading();
            }
            
            handleAjaxError(xhr, status, error);
            throw error;
        });
}

// ==================== CONVENIENCE FUNCTIONS ====================

/**
 * Fetch and display outlets in dropdown
 * @param {string} selectId - Select element ID
 * @returns {Promise}
 */
function fetchAndPopulateOutlets(selectId) {
    return NewsTraceAPI.getOutlets().then(function(response) {
        if (response.success && response.outlets) {
            const $select = $(`#${selectId}`);
            $select.empty();
            $select.append('<option value="">Select outlet...</option>');
            
            response.outlets.forEach(outlet => {
                $select.append(`<option value="${outlet.id}">${outlet.name}</option>`);
            });
            
            return response.outlets;
        }
    });
}

/**
 * Fetch and display journalists for outlet
 * @param {number} outletId - Outlet ID
 * @param {string} containerId - Container element ID
 * @returns {Promise}
 */
function fetchAndDisplayJournalists(outletId, containerId) {
    showLoading('Loading journalists...');
    
    return NewsTraceAPI.getOutletJournalists(outletId).then(function(response) {
        hideLoading();
        
        if (response.success && response.journalists) {
            const $container = $(`#${containerId}`);
            $container.empty();
            
            response.journalists.forEach(journalist => {
                const card = createJournalistCard(journalist);
                $container.append(card);
            });
            
            return response.journalists;
        }
    }).catch(function(error) {
        hideLoading();
        showToast('Failed to load journalists', 'error');
    });
}

/**
 * Create journalist card HTML
 * @param {Object} journalist - Journalist data
 * @returns {string} HTML string
 */
function createJournalistCard(journalist) {
    return `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="gradient-card h-100">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <h5 class="fw-bold mb-0">${journalist.name}</h5>
                    <span class="badge bg-primary">${(journalist.influence_score || 0).toFixed(0)}</span>
                </div>
                
                <p class="text-muted mb-2">
                    <i class="fas fa-briefcase me-2"></i>${journalist.beat || 'General'}
                </p>
                
                ${journalist.contact_email ? `
                    <p class="text-muted mb-2">
                        <i class="fas fa-envelope me-2"></i>
                        <a href="mailto:${journalist.contact_email}" class="text-decoration-none">
                            ${journalist.contact_email}
                        </a>
                    </p>
                ` : ''}
                
                ${journalist.twitter_handle ? `
                    <p class="text-muted mb-2">
                        <i class="fab fa-twitter me-2"></i>
                        <a href="https://twitter.com/${journalist.twitter_handle.replace('@', '')}" 
                           target="_blank" class="text-decoration-none">
                            ${journalist.twitter_handle}
                        </a>
                    </p>
                ` : ''}
                
                ${journalist.bio ? `
                    <p class="small text-muted mt-3" style="line-height: 1.6;">
                        ${truncateText(journalist.bio, 100)}
                    </p>
                ` : ''}
                
                ${journalist.profile_url ? `
                    <a href="${journalist.profile_url}" target="_blank" 
                       class="btn btn-sm btn-outline-light mt-3">
                        <i class="fas fa-external-link-alt me-2"></i>View Profile
                    </a>
                ` : ''}
            </div>
        </div>
    `;
}

// ==================== EXPORT MODULE ====================

// Make API available globally
window.NewsTraceAPI = NewsTraceAPI;
window.safeAPICall = safeAPICall;
window.fetchAndPopulateOutlets = fetchAndPopulateOutlets;
window.fetchAndDisplayJournalists = fetchAndDisplayJournalists;

console.log('[LOADED] API.js module loaded successfully');
