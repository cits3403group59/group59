function generateTwinChart() {
    const ctx = document.getElementById('twinChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Filled', 'Remaining'],
            datasets: [{
                data: [60, 40],
                backgroundColor: ['#4CAF50', '#E0E0E0'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    generateTwinChart();
});