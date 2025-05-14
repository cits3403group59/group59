// Fetch data from your Flask API using get_friend_data
async function fetchFriendData(userId) {
    // save friend id in local storage so data persistss
    localStorage.setItem('selectedFriendId', userId);

    const url = `/api/userdata/${userId}`

    try {
        const response = await fetch(url);
        const data = await response.json();
        console.log(data)
        renderCharts(data);  // Once data is fetched, render the charts
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

let sleepChartInstance = null;
let coffeeChartInstance = null;
let dailyStepsChartInstance = null;
let alcoholChartInstance = null;
let wakeUpTimeChartInstance = null;
let bedTimeChartInstance = null;
let exerciseChartInstance = null;
let moneyChartInstance = null;
let moodChartInstance = null;
let screenTimeChartInstance = null;
let socialMediaChartInstance = null;
let socialTimeChartInstance = null;
let studyTimeChartInstance = null;
let transportationChartInstance = null;
let workTimeChartInstance = null;


// Render the charts using Chart.js
function renderCharts(data) {
    // Prepare data for the charts
    const dates = data.map(d => d.date);
    const sleepData = data.map(d => d.sleep_hours);
    const coffeeData = data.map(d => d.coffee_intake);
    const stepsData = data.map(d => d.daily_steps);
    const alcoholData = data.map(d => d.alcohol);
    const bedTimeData = data.map(d => d.bed_time);
    const exerciseData = data.map(d => d.exercise_hours);
    const moneyData = data.map(d => d.money_spent);
    const moodData = data.map(d => d.mood);
    const screenTimeData = data.map(d => d.screen_time);
    const socialMediaData = data.map(d => d.social_media);
    const socialTimeData = data.map(d => d.social_time);
    const studyTimeData = data.map(d => d.study_time);
    const transportationData = data.map(d => d.transportation);
    const wakeUpTimeData = data.map(d => d.wake_up_time);
    const workTimeData = data.map(d => d.work_time);

    // map time values into human readable values

    function timeToMinutes(timeString) {
        const [hours, minutes] = timeString.split(':').map(Number);
        return hours * 60 + minutes;
    }

    const bedTimes = bedTimeData.map(timeToMinutes);
    const wakeUpTimes = wakeUpTimeData.map(timeToMinutes);

    // destroy previous instances if any
    if (sleepChartInstance) sleepChartInstance.destroy();
    if (coffeeChartInstance) coffeeChartInstance.destroy();
    if (dailyStepsChartInstance) dailyStepsChartInstance.destroy();
    if (alcoholChartInstance) alcoholChartInstance.destroy();
    if (wakeUpTimeChartInstance) wakeUpTimeChartInstance.destroy();
    if (bedTimeChartInstance) bedTimeChartInstance.destroy();
    if (exerciseChartInstance) exerciseChartInstance.destroy();
    if (moneyChartInstance) moneyChartInstance.destroy();
    if (moodChartInstance) moodChartInstance.destroy();
    if (screenTimeChartInstance) screenTimeChartInstance.destroy();
    if (socialMediaChartInstance) socialMediaChartInstance.destroy();
    if (socialTimeChartInstance) socialTimeChartInstance.destroy();
    if (studyTimeChartInstance) studyTimeChartInstance.destroy();
    if (transportationChartInstance) transportationChartInstance.destroy();
    if (workTimeChartInstance) workTimeChartInstance.destroy();

    // Chart for Sleep Hours
    const sleepHoursCtx = document.getElementById('sleepHoursChart').getContext('2d');
    sleepChartInstance = new Chart(sleepHoursCtx, {
        type: 'line',  // You can use 'line', 'line', etc.
        data: {
            labels: dates,
            datasets: [{
                label: 'Hours Slept',
                data: sleepData,
                borderColor: '#fa3980',
                fill: false
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                }
            }
        }
    });

    // Chart for Coffee Intake
    const coffeeIntakeCtx = document.getElementById('coffeeIntakeChart').getContext('2d');
    coffeeChartInstance = new Chart(coffeeIntakeCtx, {
        type: 'line',  // Use line chart
        data: {
            labels: dates,
            datasets: [{
                label: 'Coffee Intake (Cups)',
                data: coffeeData,
                borderColor: '#fa3980'
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Coffee Intake (Shots)'
                    }
                }
            }
        }
    });

    // Chart for Daily Steps
    const dailyStepsCtx = document.getElementById('dailyStepsChart').getContext('2d');
    dailyStepsChartInstance =  new Chart(dailyStepsCtx, {
        type: 'line',  // Use line chart for daily steps
        data: {
            labels: dates,
            datasets: [{
                label: 'Daily Steps',
                data: stepsData,
                borderColor: '#fa3980'
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Steps'
                    }
                }
            }
        }
    });

    // Chart for Alcohol Consumption
    const alcoholCtx = document.getElementById('alcoholChart').getContext('2d');
    alcoholChartInstance = new Chart(alcoholCtx, {
        type: 'line',  // Use line chart for alcohol consumption
        data: {
            labels: dates,
            datasets: [{
                label: 'Alcohol Consumption (Standard Drinks)',
                data: alcoholData,
                borderColor: '#fa3980'
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Dates'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Standard Drinks'
                    }
                }
            }
        }
    });

    // Chart for Wake Up Time
    const wakeUpTimeCtx = document.getElementById('wakeUpTimeChart').getContext('2d');
    wakeUpTimeChartInstance = new Chart(wakeUpTimeCtx, {
        type: 'line',  // Use line chart for bed time
        data: {
            labels: dates,
            datasets: [{
                label: 'Wake Up Time',
                data: wakeUpTimes,
                borderColor: '#fa3980',
                fill: false
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const value = context.parsed.y;
                            const hours = Math.floor(value / 60);
                            const minutes = value % 60;
                            return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Time (24hr)',
                    },
                    ticks: {
                        stepsize: 10,
                        callback: function (value) {
                            const h = Math.floor(value / 60);
                            const m = value % 60;
                            return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
                        }
                    }
                }
            }
        }
    });
    // Chart for Bed Time
    const bedTimeCtx = document.getElementById('bedTimeChart').getContext('2d');
    bedTimeChartInstance = new Chart(bedTimeCtx, {
        type: 'line',  // Use line chart for bed time
        data: {
            labels: dates,
            datasets: [{
                label: 'Bed Time',
                data: bedTimes,
                borderColor: '#fa3980',
                fill: false
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const value = context.parsed.y;
                            const hours = Math.floor(value / 60);
                            const minutes = value % 60;
                            return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Time (24hr)',
                    },
                    ticks: {
                        stepsize: 10,
                        callback: function (value) {
                            const h = Math.floor(value / 60);
                            const m = value % 60;
                            return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
                        }
                    }
                }
            }
        }
    });

    // Chart for Exercise Hours
    const exerciseCtx = document.getElementById('exerciseChart').getContext('2d');
    exerciseChartInstance = new Chart(exerciseCtx, {
        type: 'line',  // Use line chart for exercise minutes
        data: {
            labels: dates,
            datasets: [{
                label: 'Exercise Hours',
                data: exerciseData,
                borderColor: '#fa3980'
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Dates'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                }
            }
        }
    });
    // Chart for Money Spent
    const moneyCtx = document.getElementById('moneyChart').getContext('2d');
    moneyChartInstance = new Chart(moneyCtx, {
        type: 'line',  // Use line chart for money spent
        data: {
            labels: dates,
            datasets: [{
                label: 'Money Spent ($)',
                data: moneyData,
                borderColor: '#fa3980'
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Dates'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Amount Spent (AUD)'
                    }
                }
            }
        }
    });

    // Card for Mood
    const moodCounts = moodData.reduce((acc, app) => {
        acc[app] = (acc[app] || 0) + 1;
        return acc;
    }, {});

    console.log(moodCounts);

    const moodLabels = Object.keys(moodCounts); // app names
    const moodFreq = Object.values(moodCounts); // frequency of most used app

    const moodCtx = document.getElementById('moodChart');
    moodChartInstance = new Chart(moodCtx, {
        type: 'bar',
        data: {
            labels: moodLabels,
            datasets: [{
                label: '',
                data: moodFreq,
                backgroundColor: '#fa3980'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            // Customizing the tooltip message to show app frequency
                            return tooltipItem.label + ': ' + tooltipItem.raw + ' times';  // e.g., "Facebook: 2 times"
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Mood'
                    },
                    beginAtZero: true
                },
                y: {
                    title: {
                        display: true,
                        text: 'Frequency'
                    },
                    beginAtZero: true
                }
            }
        }
    });

    console.log(screenTimeData);
    // Chart for Screen Time
    const screenTimeCtx = document.getElementById('screenTimeChart').getContext('2d');
    screenTimeChartInstance = new Chart(screenTimeCtx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Screen Time (Hours)',
                data: screenTimeData,
                borderColor: '#fa3980'
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Dates'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                }
            }
        }
    });

    // Chart for Social Media Usage
    const appCounts = socialMediaData.reduce((acc, app) => {
        acc[app] = (acc[app] || 0) + 1;
        return acc;
    }, {});

    console.log(appCounts);

    const appLabels = Object.keys(appCounts); // app names
    const appFreq = Object.values(appCounts); // frequency of most used app

    const socialMediaCtx = document.getElementById('socialMediaChart').getContext('2d');
    socialMediaChartInstance = new Chart(socialMediaCtx, {
        type: 'bar',
        data: {
            labels: appLabels,
            datasets: [{
                label: 'Most Used App',
                data: appFreq,
                backgroundColor: '#fa3980'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            // Customizing the tooltip message to show app frequency
                            return tooltipItem.label + ': ' + tooltipItem.raw + ' times';  // e.g., "Facebook: 2 times"
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Social Media App'
                    },
                    beginAtZero: true
                },
                y: {
                    title: {
                        display: true,
                        text: 'Frequency'
                    },
                    beginAtZero: true
                }
            }
        }
    });
    // Chart for Social Time
    const socialTimeCtx = document.getElementById('socialTimeChart').getContext('2d');
    socialTimeChartInstance = new Chart(socialTimeCtx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Social Time (Hours)',
                data: socialTimeData,
                borderColor: '#fa3980'
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
    // Chart for Study Time
    const studyTimeCtx = document.getElementById('studyTimeChart').getContext('2d');
    studyTimeChartInstance = new Chart(studyTimeCtx, {
        type: 'line',  // Use line chart for study time
        data: {
            labels: dates,
            datasets: [{
                label: 'Study Time (Hours)',
                data: studyTimeData,
                borderColor: '#fa3980'
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
    // Chart for Transportation
    const transportCounts = transportationData.reduce((acc, app) => {
        acc[app] = (acc[app] || 0) + 1;
        return acc;
    }, {});

    console.log(transportCounts);

    const transLabels = Object.keys(transportCounts); // app names
    const transFreq = Object.values(transportCounts); // frequency of most used app

    const transportationCtx = document.getElementById('transportationChart').getContext('2d');
    transportationChartInstance = new Chart(transportationCtx, {
        type: 'bar',
        data: {
            labels: transLabels,
            datasets: [{
                label: 'Mode of Transport',
                data: transFreq,
                backgroundColor: '#fa3980'
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Mode of Transport'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Freuquency'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            // Customizing the tooltip message to show app frequency
                            return tooltipItem.label + ': ' + tooltipItem.raw + ' times';  // e.g., "Facebook: 2 times"
                        }
                    }
                }
            }
        }
    });

    // Chart for Work Time
    const workTimeCtx = document.getElementById('workTimeChart').getContext('2d');
    workTimeChartInstance = new Chart(workTimeCtx, {
        type: 'line',  // Use line chart for work time
        data: {
            labels: dates,
            datasets: [{
                label: 'Work Time (Hours)',
                data: workTimeData,
                borderColor: '#fa3980'
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}


async function fetchFriends() {
    try {
        const res = await fetch(`/get_friends`);
        const friends = await res.json();

        const listContainer = document.getElementById('friend-list-content');
        listContainer.innerHTML = '';

        if (friends.length === 0) {
            listContainer.innerHTML = '<p class="text-gray-500 text-sm">No friends found.</p>';
            return;
        }

        friends.forEach(friend => {
            const friendHTML = `
            <div class="flex justify-between items-center mb-4 hover:bg-gray-100 p-2 rounded-lg group relative">
                <div>
                    <p class="font-bold">${friend.first_name} ${friend.last_name}</p>
                    <p class="text-sm text-gray-500">${friend.email}</p>
                </div>
                <button class="text-sm text-[#FA3980] hover:text-pink-600 font-semibold" onclick="fetchFriendData(${friend.id})">
                    Get Data
                </button>
            </div>
        `;

            listContainer.insertAdjacentHTML('beforeend', friendHTML);
        });
    } catch (error) {
        console.error("Failed to fetch friends:", error);
        document.getElementById('friend-list').innerHTML = '<p class="text-red-500 text-sm">Failed to load friends.</p>';
    }
}

// Load friends on page load
fetchFriends();
document.addEventListener('DOMContentLoaded', () => {
    const selectedFriendId = localStorage.getItem('selectedFriendId');
    if (selectedFriendId) {
        fetchFriendData(selectedFriendId);
    }
});