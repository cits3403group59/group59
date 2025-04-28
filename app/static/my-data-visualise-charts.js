function renderBarChart() {
    const ctx1 = document.getElementById('chart1').getContext('2d');
    new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            datasets: [{
                label: 'Workouts',
                data: [1, 0, 1, 1, 0],
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function renderLineChart() {
    const ctx2 = document.getElementById('chart2').getContext('2d');
    new Chart(ctx2, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            datasets: [{
                label: 'Water Intake (L)',
                data: [2, 2.5, 1.8, 2.2, 2],
                fill: false,
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.3
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function renderPieChart() {
    const ctx3 = document.getElementById('chart3').getContext('2d');
    new Chart(ctx3, {
        type: 'pie',
        data: {
            labels: ['Good', 'Average', 'Poor'],
            datasets: [{
                label: 'Sleep Quality',
                data: [60, 25, 15],
                backgroundColor: [
                    'rgba(75, 192, 75, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(255, 99, 132, 0.7)'
                ],
                borderColor: [
                    'rgba(75, 192, 75, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {}
    });
}

function renderStudyHoursChart() {
    const ctx = document.getElementById('studyHoursChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Hours Studied',
                data: [2, 3, 4, 2, 1, 5, 0],
                backgroundColor: 'rgba(255, 99, 132, 0.7)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function renderRunningDistanceChart() {
    const ctx = document.getElementById('runningDistanceChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Kilometers Run',
                data: [10, 15, 7, 20],
                fill: false,
                borderColor: 'rgba(54, 162, 235, 1)',
                tension: 0.3
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function renderDietTypeChart() {
    const ctx = document.getElementById('dietTypeChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Vegetarian', 'Vegan', 'Omnivore'],
            datasets: [{
                data: [30, 20, 50],
                backgroundColor: [
                    'rgba(255, 205, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(255, 99, 132, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 205, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {}
    });
}

function renderSleepStagesChart() {
    const ctx = document.getElementById('sleepStagesChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Deep Sleep', 'Light Sleep', 'REM', 'Awake'],
            datasets: [{
                data: [40, 35, 20, 5],
                backgroundColor: [
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(255, 99, 132, 0.7)'
                ],
                borderColor: [
                    'rgba(153, 102, 255, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {}
    });
}

function renderBooksReadChart() {
    const ctx = document.getElementById('booksReadChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['January', 'February', 'March', 'April'],
            datasets: [{
                label: 'Books Read',
                data: [2, 4, 3, 5],
                backgroundColor: 'rgba(255, 159, 64, 0.7)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y', // Makes it horizontal
            scales: {
                x: { beginAtZero: true }
            }
        }
    });
}

function renderScreenTimeChart() {
    const ctx = document.getElementById('screenTimeChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            datasets: [{
                label: 'Screen Time (hours)',
                data: [3, 4, 5, 2, 6, 7, 4],
                fill: false,
                borderColor: 'rgba(153, 102, 255, 1)',
                tension: 0.3
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function renderDailyStepChart() {
    const ctx = document.getElementById('dailyStepsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            datasets: [{
                label: 'Steps Taken',
                data: [8000, 7500, 9000, 10000, 8500, 12000, 11000],
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}
// Render charts only after DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    renderBarChart();
    renderLineChart();
    renderPieChart();
    renderStudyHoursChart();
    renderRunningDistanceChart();
    renderDietTypeChart();
    renderSleepStagesChart();
    renderBooksReadChart();
    renderScreenTimeChart();
    renderDailyStepChart();
});
