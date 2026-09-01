// Bias & Sentiment Radar Chart Component
function renderBiasRadar(containerId, biasData) {
    if (typeof Plotly === 'undefined') return;
    const data = [{
        type: 'scatterpolar',
        r: [biasData.sentiment || 50, biasData.objectivity || 70, biasData.citation_depth || 80, biasData.readability || 65, biasData.clickbait_avoidance || 85],
        theta: ['Sentiment Balance', 'Objectivity', 'Citation Depth', 'Readability', 'Factuality'],
        fill: 'toself',
        fillcolor: 'rgba(0, 242, 254, 0.2)',
        line: { color: '#00f2fe' }
    }];
    const layout = {
        polar: { radialaxis: { visible: true, range: [0, 100] } },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        margin: { t: 30, b: 30, l: 30, r: 30 }
    };
    Plotly.newPlot(containerId, data, layout, { displayModeBar: false });
}
