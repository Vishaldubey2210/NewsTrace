/**
 * NewsTrace Compare Page JavaScript
 * Outlet comparison functionality
 */

let beatComparisonChart;
let outlets = [];
let outlet1Data = null;
let outlet2Data = null;

$(document).ready(function() {
    console.log('[COMPARE] Initializing...');
    
    // Load outlets
    loadOutlets();
    
    // Compare button
    $('#compareBtn').on('click', function() {
        const outlet1Id = $('#outlet1Select').val();
        const outlet2Id = $('#outlet2Select').val();
        
        if (!outlet1Id || !outlet2Id) {
            alert('Please select both outlets');
            return;
        }
        
        if (outlet1Id === outlet2Id) {
            alert('Please select different outlets');
            return;
        }
        
        compareOutlets(outlet1Id, outlet2Id);
    });
});

function loadOutlets() {
    $.ajax({
        url: '/api/outlets',
        method: 'GET',
        success: function(response) {
            if (response.success && response.outlets) {
                outlets = response.outlets;
                populateSelects(response.outlets);
            }
        },
        error: function(xhr, status, error) {
            console.error('[ERROR] Failed to load outlets:', error);
        }
    });
}

function populateSelects(outlets) {
    const select1 = $('#outlet1Select');
    const select2 = $('#outlet2Select');
    
    select1.empty().append('<option value="">Select first outlet...</option>');
    select2.empty().append('<option value="">Select second outlet...</option>');
    
    outlets.forEach(outlet => {
        const option = `<option value="${outlet.id}">${outlet.name}</option>`;
        select1.append(option);
        select2.append(option);
    });
}

function compareOutlets(outlet1Id, outlet2Id) {
    console.log('[COMPARE] Comparing outlets:', outlet1Id, 'vs', outlet2Id);
    
    // Show loading
    $('#comparisonResults').hide();
    
    // Load data for both outlets
    Promise.all([
        loadOutletData(outlet1Id),
        loadOutletData(outlet2Id)
    ]).then(([data1, data2]) => {
        outlet1Data = data1;
        outlet2Data = data2;
        
        displayComparison(data1, data2);
    }).catch(error => {
        console.error('[ERROR] Comparison failed:', error);
        alert('Failed to load outlet data');
    });
}

function loadOutletData(outletId) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/api/outlet/' + outletId + '/journalists',
            method: 'GET',
            success: function(response) {
                if (response.success) {
                    resolve({
                        outletId: outletId,
                        outlet: outlets.find(o => o.id == outletId),
                        journalists: response.journalists
                    });
                } else {
                    reject('Failed to load outlet data');
                }
            },
            error: reject
        });
    });
}

function displayComparison(data1, data2) {
    console.log('[COMPARE] Displaying comparison');
    
    // Update outlet names
    $('#outlet1Name, #outlet1NameTop').text(data1.outlet.name);
    $('#outlet2Name, #outlet2NameTop').text(data2.outlet.name);
    
    // Calculate stats
    const stats1 = calculateStats(data1.journalists);
    const stats2 = calculateStats(data2.journalists);
    
    // Display stats
    displayStats(1, stats1);
    displayStats(2, stats2);
    
    // Display charts
    displayBeatComparison(data1.journalists, data2.journalists, data1.outlet.name, data2.outlet.name);
    
    // Display top journalists
    displayTopJournalists(1, data1.journalists);
    displayTopJournalists(2, data2.journalists);
    
    // Find cross-outlet matches
    findCrossOutletMatches(data1.journalists, data2.journalists);
    
    // Show results
    $('#comparisonResults').fadeIn();
}

function calculateStats(journalists) {
    const total = journalists.length;
    const avgInfluence = total > 0 ? 
        journalists.reduce((sum, j) => sum + (j.influence_score || 0), 0) / total : 0;
    const beats = [...new Set(journalists.map(j => j.beat).filter(b => b))];
    const withContact = journalists.filter(j => j.contact_email).length;
    
    return {
        total,
        avgInfluence: avgInfluence.toFixed(1),
        beats: beats.length,
        withContact
    };
}

function displayStats(outletNum, stats) {
    $(`#outlet${outletNum}Journalists`).text(stats.total);
    $(`#outlet${outletNum}AvgInfluence`).text(stats.avgInfluence);
    $(`#outlet${outletNum}Beats`).text(stats.beats);
    $(`#outlet${outletNum}Contact`).text(stats.withContact);
}

function displayBeatComparison(journalists1, journalists2, name1, name2) {
    // Get all unique beats
    const allBeats = [...new Set([
        ...journalists1.map(j => j.beat || 'General'),
        ...journalists2.map(j => j.beat || 'General')
    ])];
    
    // Count beats for each outlet
    const counts1 = {};
    const counts2 = {};
    
    allBeats.forEach(beat => {
        counts1[beat] = journalists1.filter(j => (j.beat || 'General') === beat).length;
        counts2[beat] = journalists2.filter(j => (j.beat || 'General') === beat).length;
    });
    
    // Destroy existing chart
    if (beatComparisonChart) {
        beatComparisonChart.destroy();
    }
    
    // Create chart
    const ctx = document.getElementById('beatComparisonChart');
    beatComparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: allBeats,
            datasets: [
                {
                    label: name1,
                    data: allBeats.map(beat => counts1[beat]),
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                },
                {
                    label: name2,
                    data: allBeats.map(beat => counts2[beat]),
                    backgroundColor: 'rgba(240, 147, 251, 0.6)',
                    borderColor: 'rgba(240, 147, 251, 1)',
                    borderWidth: 1
                }
            ]
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

function displayTopJournalists(outletNum, journalists) {
    const container = $(`#outlet${outletNum}TopJournalists`);
    container.empty();
    
    // Sort by influence
    const top5 = journalists
        .sort((a, b) => (b.influence_score || 0) - (a.influence_score || 0))
        .slice(0, 5);
    
    top5.forEach((j, index) => {
        const item = `
            <div class="d-flex justify-content-between align-items-center mb-2 p-2" 
                 style="background: rgba(255,255,255,0.05); border-radius: 8px;">
                <div>
                    <strong>${index + 1}. ${j.name}</strong>
                    <small class="d-block text-muted">${j.beat || 'General'}</small>
                </div>
                <span class="badge bg-primary">${(j.influence_score || 0).toFixed(0)}</span>
            </div>
        `;
        container.append(item);
    });
}

function findCrossOutletMatches(journalists1, journalists2) {
    const container = $('#crossOutletMatches');
    container.empty();
    
    const matches = [];
    
    // Simple name matching
    journalists1.forEach(j1 => {
        journalists2.forEach(j2 => {
            const similarity = calculateNameSimilarity(j1.name, j2.name);
            if (similarity > 0.8) {
                matches.push({
                    j1,
                    j2,
                    similarity
                });
            }
        });
    });
    
    if (matches.length === 0) {
        container.html('<p class="text-muted text-center">No potential matches found</p>');
        return;
    }
    
    matches.forEach(match => {
        const item = `
            <div class="alert alert-info mb-2">
                <strong>Potential Match:</strong>
                ${match.j1.name} ⇔ ${match.j2.name}
                <span class="badge bg-success float-end">${(match.similarity * 100).toFixed(0)}% Match</span>
            </div>
        `;
        container.append(item);
    });
}

function calculateNameSimilarity(name1, name2) {
    // Simple Levenshtein-like similarity
    name1 = name1.toLowerCase();
    name2 = name2.toLowerCase();
    
    if (name1 === name2) return 1.0;
    
    const longer = name1.length > name2.length ? name1 : name2;
    const shorter = name1.length > name2.length ? name2 : name1;
    
    if (longer.length === 0) return 1.0;
    
    const editDistance = levenshteinDistance(longer, shorter);
    return (longer.length - editDistance) / longer.length;
}

function levenshteinDistance(str1, str2) {
    const matrix = [];
    
    for (let i = 0; i <= str2.length; i++) {
        matrix[i] = [i];
    }
    
    for (let j = 0; j <= str1.length; j++) {
        matrix[0][j] = j;
    }
    
    for (let i = 1; i <= str2.length; i++) {
        for (let j = 1; j <= str1.length; j++) {
            if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j] + 1
                );
            }
        }
    }
    
    return matrix[str2.length][str1.length];
}
