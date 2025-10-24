/**
 * NewsTrace Network Graph Visualization
 * Uses Vis.js for interactive network rendering
 */

// Global variables
let network = null;
let currentOutletId = null;

$(document).ready(function() {
    console.log('[NETWORK] Page loaded');
    
    // Check if vis-network is loaded
    if (typeof vis === 'undefined') {
        console.error('[NETWORK] ERROR: vis-network library not loaded!');
        alert('Network visualization library failed to load. Please refresh the page.');
        return;
    }
    
    // Load outlets for selection
    loadOutlets();
    
    // Outlet selection change
    $('#outletSelect').on('change', function() {
        const outletId = $(this).val();
        if (outletId) {
            currentOutletId = outletId;
            loadNetworkGraph(outletId);
        }
    });
    
    // Layout change
    $('#layoutSelect').on('change', function() {
        if (currentOutletId) {
            loadNetworkGraph(currentOutletId);
        }
    });
    
    // Reset zoom
    $('#resetZoom').on('click', function() {
        if (network) {
            network.fit();
        }
    });
    
    // Export graph
    $('#exportGraph').on('click', function() {
        if (network) {
            // Implementation for export
            alert('Export functionality - Coming soon!');
        }
    });
    
    // Search filter
    $('#searchFilter').on('input', function() {
        const searchTerm = $(this).val().toLowerCase();
        if (network && searchTerm) {
            // Filter nodes
            const allNodes = network.body.data.nodes.get();
            const matchingNodes = allNodes.filter(node => 
                node.label.toLowerCase().includes(searchTerm)
            );
            
            if (matchingNodes.length > 0) {
                network.selectNodes(matchingNodes.map(n => n.id));
                network.focus(matchingNodes[0].id, {
                    scale: 1.5,
                    animation: true
                });
            }
        }
    });
    
    // Clear filter
    $('#clearFilter').on('click', function() {
        $('#searchFilter').val('');
        if (network) {
            network.unselectAll();
            network.fit();
        }
    });
});

function loadOutlets() {
    console.log('[NETWORK] Loading outlets...');
    
    $.ajax({
        url: '/api/outlets',
        method: 'GET',
        success: function(response) {
            if (response.success && response.outlets) {
                const select = $('#outletSelect');
                select.empty();
                select.append('<option value="">Select an outlet...</option>');
                
                response.outlets.forEach(outlet => {
                    select.append(`<option value="${outlet.id}">${outlet.name}</option>`);
                });
                
                console.log('[NETWORK] Loaded ' + response.outlets.length + ' outlets');
            }
        },
        error: function(xhr, status, error) {
            console.error('[NETWORK] Error loading outlets:', error);
            $('#outletSelect').html('<option value="">Error loading outlets</option>');
        }
    });
}

function loadNetworkGraph(outletId) {
    console.log('[NETWORK] Loading graph for outlet:', outletId);
    
    // Show loading state
    $('#networkContainer').html('<div style="display: flex; align-items: center; justify-content: center; height: 600px;"><div class="text-center"><div class="loading-spinner mb-3"></div><p class="text-muted">Loading network graph...</p></div></div>');
    
    $.ajax({
        url: '/api/network/graph/' + outletId,
        method: 'GET',
        success: function(response) {
            console.log('[NETWORK] Graph data received:', response);
            
            if (response.success) {
                if (response.nodes && response.nodes.length > 0) {
                    renderNetwork(response.nodes, response.edges, response.stats);
                } else {
                    $('#networkContainer').html('<div style="display: flex; align-items: center; justify-content: center; height: 600px;"><div class="text-center"><i class="fas fa-project-diagram fa-3x mb-3" style="color: rgba(255,255,255,0.2);"></i><h5>No Data Available</h5><p class="text-muted">No journalists found for this outlet</p></div></div>');
                }
            } else {
                console.error('[NETWORK] API returned error:', response.error);
                $('#networkContainer').html('<div style="display: flex; align-items: center; justify-content: center; height: 600px;"><div class="text-center text-danger"><i class="fas fa-exclamation-triangle fa-3x mb-3"></i><h5>Error Loading Graph</h5><p>' + (response.error || 'Unknown error') + '</p></div></div>');
            }
        },
        error: function(xhr, status, error) {
            console.error('[NETWORK] AJAX Error:', error);
            console.error('[NETWORK] Response:', xhr.responseText);
            $('#networkContainer').html('<div style="display: flex; align-items: center; justify-content: center; height: 600px;"><div class="text-center text-danger"><i class="fas fa-exclamation-triangle fa-3x mb-3"></i><h5>Failed to Load Graph</h5><p>Server error: ' + error + '</p></div></div>');
        }
    });
}

function renderNetwork(nodes, edges, stats) {
    console.log('[NETWORK] Rendering graph with', nodes.length, 'nodes and', edges.length, 'edges');
    
    // Clear container
    $('#networkContainer').empty();
    
    // Update stats
    $('#nodeCount').text(stats.total_nodes || nodes.length);
    $('#edgeCount').text(stats.total_edges || edges.length);
    $('#journalistCount').text(stats.journalist_count || 0);
    $('#topicCount').text(stats.topic_count || 0);
    
    // Create data
    const data = {
        nodes: new vis.DataSet(nodes),
        edges: new vis.DataSet(edges)
    };
    
    // Get selected layout
    const layoutType = $('#layoutSelect').val() || 'physics';
    
    // Network options
    const options = {
        nodes: {
            shape: 'dot',
            size: 20,
            font: {
                size: 14,
                color: '#ffffff',
                face: 'Inter, sans-serif'
            },
            borderWidth: 2,
            borderWidthSelected: 4,
            shadow: {
                enabled: true,
                color: 'rgba(0,0,0,0.3)',
                size: 10,
                x: 2,
                y: 2
            }
        },
        edges: {
            width: 2,
            color: {
                color: 'rgba(255,255,255,0.3)',
                highlight: 'rgba(102, 126, 234, 0.8)'
            },
            smooth: {
                type: 'continuous',
                roundness: 0.5
            },
            shadow: false
        },
        physics: {
            enabled: layoutType === 'physics',
            stabilization: {
                enabled: true,
                iterations: 200
            },
            barnesHut: {
                gravitationalConstant: -2000,
                centralGravity: 0.3,
                springLength: 150,
                springConstant: 0.04,
                damping: 0.09,
                avoidOverlap: 0.5
            }
        },
        layout: layoutType === 'hierarchical' ? {
            hierarchical: {
                enabled: true,
                direction: 'UD',
                sortMethod: 'directed',
                nodeSpacing: 200,
                levelSeparation: 150
            }
        } : layoutType === 'circular' ? {
            improvedLayout: false
        } : {},
        interaction: {
            hover: true,
            tooltipDelay: 200,
            hideEdgesOnDrag: true,
            navigationButtons: true,
            keyboard: {
                enabled: true
            }
        }
    };
    
    // Create network
    const container = document.getElementById('networkContainer');
    network = new vis.Network(container, data, options);
    
    // Event listeners
    network.on('click', function(params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = data.nodes.get(nodeId);
            
            $('#selectedNode').text(node.label);
            
            // Show node details
            showNodeDetails(node, data);
        } else {
            $('#selectedNode').text('None');
            $('#nodeDetailsPanel').hide();
        }
    });
    
    network.on('stabilizationProgress', function(params) {
        const progress = Math.round((params.iterations / params.total) * 100);
        console.log('[NETWORK] Stabilization progress:', progress + '%');
    });
    
    network.on('stabilizationIterationsDone', function() {
        console.log('[NETWORK] Stabilization complete');
        network.setOptions({ physics: false });
    });
    
    console.log('[NETWORK] Network graph rendered successfully');
}

function showNodeDetails(node, data) {
    const neighbors = network.getConnectedNodes(node.id);
    const edges = network.getConnectedEdges(node.id);
    
    let detailsHTML = `
        <div class="row">
            <div class="col-md-6">
                <h6 class="fw-bold mb-2">${node.label}</h6>
                <p class="mb-1"><strong>Type:</strong> ${node.group}</p>
                <p class="mb-1"><strong>Connections:</strong> ${neighbors.length}</p>
            </div>
            <div class="col-md-6">
                <h6 class="fw-bold mb-2">Connected Nodes:</h6>
                <ul class="list-unstyled mb-0">
    `;
    
    neighbors.slice(0, 5).forEach(neighborId => {
        const neighbor = data.nodes.get(neighborId);
        if (neighbor) {
            detailsHTML += `<li><span class="badge bg-secondary me-2">${neighbor.group}</span>${neighbor.label}</li>`;
        }
    });
    
    if (neighbors.length > 5) {
        detailsHTML += `<li class="text-muted">... and ${neighbors.length - 5} more</li>`;
    }
    
    detailsHTML += `
                </ul>
            </div>
        </div>
    `;
    
    $('#nodeDetails').html(detailsHTML);
    $('#nodeDetailsPanel').show();
}
