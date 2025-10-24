/**
 * NewsTrace Analytics JavaScript - ENHANCED VERSION
 * Advanced charts and visualizations with Chart.js and Plotly
 * Version: 2.0
 */

let beatChart, influenceChart, outletChart, timelineChart;
let allJournalists = [];
let allOutlets = [];

// ==================== INITIALIZATION ====================

$(document).ready(function() {
    console.log('[ANALYTICS] Initializing analytics...');
    
    // Set Chart.js defaults
    setupChartDefaults();
    
    // Load analytics data
    loadAnalyticsData();
});

// ==================== CHART DEFAULTS ====================

function setupChartDefaults() {
    Chart.defaults.color = '#e0e0e0';
    Chart.defaults.borderColor = 'rgba(255,255,255,0.1)';
    Chart.defaults.font.family = 'Inter, system-ui, sans-serif';
}

// ==================== LOAD DATA ====================

function loadAnalyticsData() {
    console.log('[ANALYTICS] Loading data...');
    
    showLoading('Loading Analytics...', 'Fetching statistics and data');
    
    // Load stats
    $.ajax({
        url: '/api/analytics/stats',
        method: 'GET',
        success: function(response) {
            if (response.success) {
                updateStats(response.stats);
            }
        },
        error: function(xhr, status, error) {
            console.error('[ERROR] Failed to load stats:', error);
        }
    });
    
    // Load outlets
    $.ajax({
        url: '/api/outlets',
        method: 'GET',
        success: function(response) {
            hideLoading();
            
            if (response.success && response.outlets) {
                allOutlets = response.outlets;
                loadJournalistsForAnalytics(response.outlets);
            } else {
                showToast('No data available. Please profile some outlets first.', 'warning');
            }
        },
        error: function(xhr, status, error) {
            hideLoading();
            console.error('[ERROR] Failed to load outlets:', error);
            handleAjaxError(xhr, status, error);
        }
    });
}

// ==================== UPDATE STATISTICS ====================

function updateStats(stats) {
    $('#totalOutlets').text(stats.total_outlets || 0);
    $('#totalJournalists').text(stats.total_journalists || 0);
    
    // Calculate averages
    const avgInfluence = stats.total_journalists > 0 ? 
        Math.round((stats.total_journalists * 50) / stats.total_outlets) : 0;
    $('#avgInfluence').text(avgInfluence);
    
    // Placeholder for cross-outlet
    $('#crossOutlet').text(stats.cross_outlet_matches || 0);
}

// ==================== LOAD JOURNALISTS ====================

function loadJournalistsForAnalytics(outlets) {
    console.log('[ANALYTICS] Loading journalists for', outlets.length, 'outlets');
    
    allJournalists = [];
    let completedRequests = 0;
    
    if (outlets.length === 0) {
        renderEmptyState();
        return;
    }
    
    outlets.forEach(outlet => {
        $.ajax({
            url: '/api/outlet/' + outlet.id + '/journalists',
            method: 'GET',
            success: function(response) {
                if (response.success && response.journalists) {
                    // Add outlet info to each journalist
                    response.journalists.forEach(j => {
                        j.outlet_name = outlet.name;
                        j.outlet_id = outlet.id;
                    });
                    allJournalists = allJournalists.concat(response.journalists);
                }
                
                completedRequests++;
                
                if (completedRequests === outlets.length) {
                    console.log('[ANALYTICS] Total journalists loaded:', allJournalists.length);
                    renderCharts();
                }
            },
            error: function(xhr, status, error) {
                completedRequests++;
                console.error('[ERROR] Failed to load journalists for outlet:', outlet.id);
                
                if (completedRequests === outlets.length) {
                    renderCharts();
                }
            }
        });
    });
}

// ==================== RENDER ALL CHARTS ====================

function renderCharts() {
    if (allJournalists.length === 0) {
        renderEmptyState();
        return;
    }
    
    console.log('[ANALYTICS] Rendering charts...');
    
    renderBeatChart();
    renderInfluenceChart();
    renderOutletChart();
    renderHeatmap();
    loadTopJournalists();
    
    showToast('Analytics loaded successfully!', 'success', 3000);
}

function renderEmptyState() {
    $('.gradient-card').each(function() {
        if ($(this).find('canvas').length > 0) {
            $(this).find('canvas').parent().html(`
                <div class="text-center text-muted p-5">
                    <i class="fas fa-chart-bar fa-3x mb-3"></i>
                    <p>No data available</p>
                    <small>Profile some news outlets to see analytics</small>
                </div>
            `);
        }
    });
}

// ==================== BEAT DISTRIBUTION CHART ====================

function renderBeatChart() {
    const beatCounts = {};
    
    allJournalists.forEach(j => {
        const beat = j.beat || 'General';
        beatCounts[beat] = (beatCounts[beat] || 0) + 1;
    });
    
    const labels = Object.keys(beatCounts);
    const data = Object.values(beatCounts);
    
    const ctx = document.getElementById('beatChart');
    
    if (!ctx) {
        console.error('[ERROR] beatChart canvas not found');
        return;
    }
    
    // Destroy existing chart
    if (beatChart) {
        beatChart.destroy();
    }
    
    beatChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#667eea', '#764ba2', '#f093fb', '#f5576c',
                    '#4facfe', '#00f2fe', '#43e97b', '#38f9d7',
                    '#fa709a', '#fee140', '#30cfd0', '#330867'
                ],
                borderWidth: 2,
                borderColor: '#1a1a2e'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#e0e0e0',
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// ==================== INFLUENCE SCORE CHART ====================

function renderInfluenceChart() {
    const bins = {
        '0-20': 0,
        '20-40': 0,
        '40-60': 0,
        '60-80': 0,
        '80-100': 0
    };
    
    allJournalists.forEach(j => {
        const score = j.influence_score || 0;
        if (score < 20) bins['0-20']++;
        else if (score < 40) bins['20-40']++;
        else if (score < 60) bins['40-60']++;
        else if (score < 80) bins['60-80']++;
        else bins['80-100']++;
    });
    
    const ctx = document.getElementById('influenceChart');
    
    if (!ctx) return;
    
    if (influenceChart) {
        influenceChart.destroy();
    }
    
    influenceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(bins),
            datasets: [{
                label: 'Number of Journalists',
                data: Object.values(bins),
                backgroundColor: 'rgba(102, 126, 234, 0.7)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#e0e0e0',
                        stepSize: 1
                    },
                    grid: {
                        color: 'rgba(255,255,255,0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#e0e0e0'
                    },
                    grid: {
                        color: 'rgba(255,255,255,0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#e0e0e0'
                    }
                }
            }
        }
    });
}

// ==================== OUTLET COMPARISON CHART ====================

function renderOutletChart() {
    const outletCounts = {};
    
    allJournalists.forEach(j => {
        const outletName = j.outlet_name || 'Unknown';
        outletCounts[outletName] = (outletCounts[outletName] || 0) + 1;
    });
    
    const labels = Object.keys(outletCounts);
    const data = Object.values(outletCounts);
    
    const ctx = document.getElementById('outletChart');
    
    if (!ctx) return;
    
    if (outletChart) {
        outletChart.destroy();
    }
    
    outletChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Journalists',
                data: data,
                backgroundColor: 'rgba(240, 147, 251, 0.7)',
                borderColor: 'rgba(240, 147, 251, 1)',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        color: '#e0e0e0'
                    },
                    grid: {
                        color: 'rgba(255,255,255,0.1)'
                    }
                },
                y: {
                    ticks: {
                        color: '#e0e0e0'
                    },
                    grid: {
                        color: 'rgba(255,255,255,0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#e0e0e0'
                    }
                }
            }
        }
    });
}

// ==================== HEATMAP (PLOTLY) ====================

function renderHeatmap() {
    const heatmapDiv = document.getElementById('heatmapChart');
    
    if (!heatmapDiv) return;
    
    // Get unique beats and outlets
    const beats = [...new Set(allJournalists.map(j => j.beat || 'General'))];
    const outlets = [...new Set(allJournalists.map(j => j.outlet_name))];
    
    // Build matrix
    const matrix = [];
    
    beats.forEach(beat => {
        const row = [];
        outlets.forEach(outlet => {
            const count = allJournalists.filter(j => 
                (j.beat || 'General') === beat && j.outlet_name === outlet
            ).length;
            row.push(count);
        });
        matrix.push(row);
    });
    
    // Create Plotly heatmap
    const data = [{
        z: matrix,
        x: outlets,
        y: beats,
        type: 'heatmap',
        colorscale: 'Viridis',
        hoverongaps: false
    }];
    
    const layout = {
        title: {
            text: 'Journalist Distribution by Beat and Outlet',
            font: { color: '#e0e0e0', size: 16 }
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        xaxis: {
            title: 'Outlets',
            color: '#e0e0e0',
            tickfont: { color: '#e0e0e0' }
        },
        yaxis: {
            title: 'Beats',
            color: '#e0e0e0',
            tickfont: { color: '#e0e0e0' }
        },
        margin: { t: 50, b: 50, l: 100, r: 50 }
    };
    
    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false
    };
    
    Plotly.newPlot(heatmapDiv, data, layout, config);
}

// ==================== TOP JOURNALISTS ====================

function loadTopJournalists() {
    const container = $('#topJournalistsList');
    
    if (!container.length) return;
    
    container.empty();
    
    if (allJournalists.length === 0) {
        container.html('<p class="text-muted text-center">No data available</p>');
        return;
    }
    
    // Sort by influence score
    const topJournalists = allJournalists
        .sort((a, b) => (b.influence_score || 0) - (a.influence_score || 0))
        .slice(0, 10);
    
    topJournalists.forEach((j, index) => {
        const item = `
            <div class="d-flex justify-content-between align-items-center mb-3 p-3" 
                 style="background: rgba(255,255,255,0.05); border-radius: 10px; animation: slideIn 0.3s ease-out;">
                <div class="d-flex align-items-center">
                    <span class="badge bg-primary me-3" 
                          style="font-size: 1.2rem; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">
                        ${index + 1}
                    </span>
                    <div>
                        <strong>${j.name}</strong>
                        <small class="d-block text-muted">
                            ${j.beat || 'General'} • ${j.outlet_name || 'Unknown'}
                        </small>
                    </div>
                </div>
                <div class="text-end">
                    <div class="stat-number" style="font-size: 1.5rem;">${(j.influence_score || 0).toFixed(0)}</div>
                    <small class="text-muted">Influence</small>
                </div>
            </div>
        `;
        container.append(item);
    });
}

// ==================== CLEANUP ====================

$(window).on('beforeunload', function() {
    // Destroy charts
    if (beatChart) beatChart.destroy();
    if (influenceChart) influenceChart.destroy();
    if (outletChart) outletChart.destroy();
});

console.log('[LOADED] Analytics.js enhanced version loaded successfully');
