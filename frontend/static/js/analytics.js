/**
 * NewsTrace Analytics JavaScript
 * Advanced charts and visualizations
 */

let beatChart, influenceChart, outletChart;

$(document).ready(function() {
    console.log('[ANALYTICS] Initializing...');
    
    // Load analytics data
    loadAnalyticsData();
    
    // Initialize charts
    initializeCharts();
});

function loadAnalyticsData() {
    console.log('[ANALYTICS] Loading data...');
    
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
    
    // Load outlets data
    $.ajax({
        url: '/api/outlets',
        method: 'GET',
        success: function(response) {
            if (response.success && response.outlets) {
                loadJournalistsForAnalytics(response.outlets);
            }
        }
    });
    
    // Load top journalists
    $.ajax({
        url: '/api/journalists/top/10',
        method: 'GET',
        success: function(response) {
            if (response.success) {
                displayTopJournalists(response.journalists);
            }
        }
    });
}

function updateStats(stats) {
    $('#totalOutlets').text(stats.total_outlets || 0);
    $('#totalJournalists').text(stats.total_journalists || 0);
    $('#avgInfluence').text('75'); // Placeholder
    $('#crossOutlet').text('12'); // Placeholder
}

function loadJournalistsForAnalytics(outlets) {
    let allJournalists = [];
    let completedRequests = 0;
    
    outlets.forEach(outlet => {
        $.ajax({
            url: '/api/outlet/' + outlet.id + '/journalists',
            method: 'GET',
            success: function(response) {
                if (response.success) {
                    allJournalists = allJournalists.concat(response.journalists);
                }
                
                completedRequests++;
                if (completedRequests === outlets.length) {
                    renderCharts(allJournalists, outlets);
                }
            }
        });
    });
}

function initializeCharts() {
    // Chart.js default config
    Chart.defaults.color = '#e0e0e0';
    Chart.defaults.borderColor = 'rgba(255,255,255,0.1)';
}

function renderCharts(journalists, outlets) {
    console.log('[ANALYTICS] Rendering charts with', journalists.length, 'journalists');
    
    // Beat Distribution Pie Chart
    renderBeatChart(journalists);
    
    // Influence Score Distribution
    renderInfluenceChart(journalists);
    
    // Outlet Comparison
    renderOutletChart(journalists, outlets);
    
    // Heatmap
    renderHeatmap(journalists);
}

function renderBeatChart(journalists) {
    const beatCounts = {};
    
    journalists.forEach(j => {
        const beat = j.beat || 'General';
        beatCounts[beat] = (beatCounts[beat] || 0) + 1;
    });
    
    const data = {
        labels: Object.keys(beatCounts),
        datasets: [{
            data: Object.values(beatCounts),
            backgroundColor: [
                '#667eea', '#764ba2', '#f093fb', '#f5576c',
                '#4facfe', '#00f2fe', '#43e97b', '#38f9d7'
            ]
        }]
    };
    
    const ctx = document.getElementById('beatChart');
    beatChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#e0e0e0' }
                }
            }
        }
    });
}

function renderInfluenceChart(journalists) {
    // Create bins for influence scores
    const bins = {
        '0-20': 0,
        '20-40': 0,
        '40-60': 0,
        '60-80': 0,
        '80-100': 0
    };
    
    journalists.forEach(j => {
        const score = j.influence_score || 0;
        if (score < 20) bins['0-20']++;
        else if (score < 40) bins['20-40']++;
        else if (score < 60) bins['40-60']++;
        else if (score < 80) bins['60-80']++;
        else bins['80-100']++;
    });
    
    const ctx = document.getElementById('influenceChart');
    influenceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(bins),
            datasets: [{
                label: 'Number of Journalists',
                data: Object.values(bins),
                backgroundColor: 'rgba(102, 126, 234, 0.6)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#e0e0e0' }
                },
                x: {
                    ticks: { color: '#e0e0e0' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#e0e0e0' }
                }
            }
        }
    });
}

function renderOutletChart(journalists, outlets) {
    const outletCounts = {};
    
    // Count journalists per outlet
    journalists.forEach(j => {
        const outletId = j.outlet_id;
        outletCounts[outletId] = (outletCounts[outletId] || 0) + 1;
    });
    
    // Get outlet names
    const labels = [];
    const data = [];
    
    outlets.forEach(outlet => {
        if (outletCounts[outlet.id]) {
            labels.push(outlet.name);
            data.push(outletCounts[outlet.id]);
        }
    });
    
    const ctx = document.getElementById('outletChart');
    outletChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Journalists',
                data: data,
                backgroundColor: 'rgba(240, 147, 251, 0.6)',
                borderColor: 'rgba(240, 147, 251, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: { color: '#e0e0e0' }
                },
                y: {
                    ticks: { color: '#e0e0e0' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#e0e0e0' }
                }
            }
        }
    });
}

function renderHeatmap(journalists) {
    // Prepare data for heatmap
    const beats = [...new Set(journalists.map(j => j.beat || 'General'))];
    const outlets = [...new Set(journalists.map(j => j.outlet_id))];
    
    const matrix = [];
    const yLabels = beats;
    const xLabels = outlets.map(id => 'Outlet ' + id);
    
    beats.forEach(beat => {
        const row = [];
        outlets.forEach(outletId => {
            const count = journalists.filter(j => 
                (j.beat || 'General') === beat && j.outlet_id === outletId
            ).length;
            row.push(count);
        });
        matrix.push(row);
    });
    
    // Create Plotly heatmap
    const data = [{
        z: matrix,
        x: xLabels,
        y: yLabels,
        type: 'heatmap',
        colorscale: 'Viridis'
    }];
    
    const layout = {
        title: {
            text: 'Journalist Distribution by Beat and Outlet',
            font: { color: '#e0e0e0' }
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        xaxis: {
            title: 'Outlets',
            color: '#e0e0e0'
        },
        yaxis: {
            title: 'Beats',
            color: '#e0e0e0'
        }
    };
    
    Plotly.newPlot('heatmapChart', data, layout, {responsive: true});
}

function displayTopJournalists(journalists) {
    const container = $('#topJournalistsList');
    container.empty();
    
    if (!journalists || journalists.length === 0) {
        container.html('<p class="text-muted text-center">No data available</p>');
        return;
    }
    
    journalists.forEach((j, index) => {
        const item = `
            <div class="d-flex justify-content-between align-items-center mb-3 p-3" 
                 style="background: rgba(255,255,255,0.05); border-radius: 10px;">
                <div class="d-flex align-items-center">
                    <span class="badge bg-primary me-3" style="font-size: 1.2rem; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">
                        ${index + 1}
                    </span>
                    <div>
                        <strong>${j.name}</strong>
                        <small class="d-block text-muted">${j.beat || 'General'}</small>
                    </div>
                </div>
                <div class="text-end">
                    <div class="stat-number" style="font-size: 1.5rem;">${j.influence_score.toFixed(0)}</div>
                    <small class="text-muted">Influence</small>
                </div>
            </div>
        `;
        container.append(item);
    });
}
