// Live Breaking News Ticker Controller
document.addEventListener('DOMContentLoaded', () => {
    const ticker = document.getElementById('news-ticker-container');
    if (!ticker) return;

    fetch('/api/analytics/stats')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                console.log("Live stats loaded for ticker:", data.stats);
            }
        })
        .catch(err => console.warn("Ticker stats fetch error:", err));
});
