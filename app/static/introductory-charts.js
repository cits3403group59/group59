// filepath: /home/oliviafitzgerald/cits3403/GroupProject/group59/app/static/introductory-charts.js

// Function to create the Time Series Chart
function createTimeSeriesChart() {
    const ctx = document.getElementById('habit-time-series').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            datasets: [
                {
                    label: 'Exercise (hours)',
                    data: [3, 4, 2, 5, 6],
                    borderColor: '#FF6384',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Sleep (hours)',
                    data: [7, 6.5, 8, 7.5, 7],
                    borderColor: '#36A2EB',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Screen Time (hours)',
                    data: [5, 6, 4, 5.5, 6.5],
                    borderColor: '#FFCE56',
                    backgroundColor: 'rgba(255, 206, 86, 0.2)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // allow it to stretch to fill height
            plugins: {
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Habit Tracking Over Time'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Weeks'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Hours'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function createTwinComparisonCharts() {
    // Common options for responsiveness
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top'
            },
            title: {
                display: true,
                text: ''
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: ''
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: ''
                }
            }
        }
    };

    // Chart 1: Bar Chart Example
    new Chart(document.getElementById('twin-comparison-chart-1'), {
        type: 'bar',
        data: {
            labels: ['Math', 'Science', 'History', 'Art'],
            datasets: [
                {
                    label: 'Twin A',
                    data: [85, 90, 78, 88],
                    backgroundColor: '#FF6384'
                },
                {
                    label: 'Twin B',
                    data: [80, 85, 82, 90],
                    backgroundColor: '#36A2EB'
                }
            ]
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                title: {
                    display: true,
                    text: 'Academic Performance Comparison'
                }
            },
            scales: {
                x: {
                    ...commonOptions.scales.x,
                    title: { display: true, text: 'Subjects' }
                },
                y: {
                    ...commonOptions.scales.y,
                    title: { display: true, text: 'Scores' }
                }
            }
        }
    });

    // Chart 2: Line Chart Example
    new Chart(document.getElementById('twin-comparison-chart-2'), {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [
                {
                    label: 'Twin A',
                    data: [6, 7, 8, 7.5],
                    borderColor: '#FF6384',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Twin B',
                    data: [7, 6.5, 7.5, 8],
                    borderColor: '#36A2EB',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                title: {
                    display: true,
                    text: 'Weekly Study Hours Comparison'
                }
            },
            scales: {
                x: {
                    ...commonOptions.scales.x,
                    title: { display: true, text: 'Weeks' }
                },
                y: {
                    ...commonOptions.scales.y,
                    title: { display: true, text: 'Hours' }
                }
            }
        }
    });

    // Chart 3: Donut Chart Example
    new Chart(document.getElementById('twin-comparison-chart-3'), {
        type: 'doughnut',
        data: {
            labels: ['Similarity', 'Difference'],
            datasets: [
                {
                    data: [75, 25], // Example similarity score: 75% similar, 25% different
                    backgroundColor: ['#36A2EB', '#FF6384']
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Similarity Score'
                }
            }
        }
    });
}

function createFriendsComparisonCharts() {
    // Common options for responsiveness
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top'
            },
            title: {
                display: true,
                text: ''
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: ''
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: ''
                }
            }
        }
    };

    // Chart 1: Bar Chart Example
    new Chart(document.getElementById('friends-comparison-chart-1'), {
        type: 'bar',
        data: {
            labels: ['Alice', 'Bob', 'Charlie', 'Daisy'],
            datasets: [
                {
                    label: 'You',
                    data: [5, 7, 6, 4],
                    backgroundColor: '#FF6384'
                },
                {
                    label: 'Friend',
                    data: [6, 5, 7, 3],
                    backgroundColor: '#36A2EB'
                }
            ]
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                title: {
                    display: true,
                    text: 'Study Hours Comparison'
                }
            },
            scales: {
                x: {
                    ...commonOptions.scales.x,
                    title: { display: true, text: 'Friend' }
                },
                y: {
                    ...commonOptions.scales.y,
                    title: { display: true, text: 'Hours' }
                }
            }
        }
    });

    // Chart 2: Line Chart Example
    new Chart(document.getElementById('friends-comparison-chart-2'), {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [
                {
                    label: 'You',
                    data: [7, 6.5, 7.5, 8, 7, 6, 6.5],
                    borderColor: '#FF6384',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Friend',
                    data: [6.5, 7, 6, 7.5, 6.8, 7, 6],
                    borderColor: '#36A2EB',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                title: {
                    display: true,
                    text: 'Sleep Pattern Comparison'
                }
            },
            scales: {
                x: {
                    ...commonOptions.scales.x,
                    title: { display: true, text: 'Day of Week' }
                },
                y: {
                    ...commonOptions.scales.y,
                    title: { display: true, text: 'Hours of Sleep' }
                }
            }
        }
    });

    // Chart 3: Radar Chart Example
    new Chart(document.getElementById('friends-comparison-chart-3'), {
        type: 'radar',
        data: {
            labels: ['Social', 'Study', 'Fitness', 'Sleep', 'Work'],
            datasets: [
                {
                    label: 'You',
                    data: [8, 7, 6, 7, 5],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: '#FF6384',
                    pointBackgroundColor: '#FF6384'
                },
                {
                    label: 'Friend',
                    data: [7, 6, 7, 6, 6],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: '#36A2EB',
                    pointBackgroundColor: '#36A2EB'
                }
            ]
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                title: {
                    display: true,
                    text: 'Lifestyle Balance Comparison'
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    pointLabels: {
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    });
}



// Call the function to create the stacked bar chart
// Ensure both charts are created after the DOM has fully loaded
document.addEventListener('DOMContentLoaded', () => {
    createTimeSeriesChart();
    createTwinComparisonCharts();
    createFriendsComparisonCharts();
});