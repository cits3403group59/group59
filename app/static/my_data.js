const valueMappings = {
  coffee_intake: {
    "None": 0,
    "1 cup": 1,
    "2 cups": 2,
    "3 cups": 3,
    "More than 3 cups": 4
  },
  daily_steps: {
    "Less than 1000": 0.5,
    "1001 - 3000": 2,
    "3001 - 5000": 4,
    "5001 - 7000": 6,
    "7001 - 9000": 8,
    "9001 - 10000": 9.5,
    "More than 10000": 11
  },
  sleep_hours: {
    "8 - 10 Hours": 9,
    // Add more as needed
  },
  screen_time: {
    "4 - 5 Hours": 4.5,
    // Add more
  },
  study_time: {
    "More than 8 hours?!?": 9
  },
  exercise_minutes: {
    "More than 1 hour and 30 minutes": 2
  },
  social_time: {
    "1 - 2 Hours": 1.5
  },
  work_time: {
    "4 - 6 Hours": 5
  }
  // Add other mappings here
};


// Fetch data from your Flask API using the get_data_between route
async function fetchData() {
    console.log(userId);
    const startDate = document.getElementById("startDate").value;  // Assuming you have a date range input
    const endDate = document.getElementById("endDate").value;
    const url = `/api/userdata/${userId}?start=${startDate}&end=${endDate}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        renderCharts(data);  // Once data is fetched, render the charts
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Render the charts using Chart.js
function renderCharts(data) {
    // Prepare data for the charts
    const sleepData = data.map(d => d.sleep_hours);  // Example field from your API response
    const coffeeData = data.map(d => d.coffee_intake);  // Example field from your API response
    const stepsData = data.map(d => d.daily_steps);  // Example field from your API response
    const dates = data.map(d => d.date);  // Example dates for the x-axis

    // Chart for Sleep Hours
    const sleepHoursCtx = document.getElementById('sleepHoursChart').getContext('2d');
    new Chart(sleepHoursCtx, {
        type: 'line',  // You can use 'bar', 'line', etc.
        data: {
            labels: dates,
            datasets: [{
                label: 'Sleep Hours',
                data: sleepData,
                borderColor: '#4CAF50',
                fill: false
            }]
        }
    });

    // Chart for Coffee Intake
    const coffeeIntakeCtx = document.getElementById('coffeeIntakeChart').getContext('2d');
    new Chart(coffeeIntakeCtx, {
        type: 'bar',  // Use bar chart
        data: {
            labels: dates,
            datasets: [{
                label: 'Coffee Intake (Cups)',
                data: coffeeData,
                backgroundColor: '#FF9800'
            }]
        }
    });

    // Chart for Daily Steps
    const dailyStepsCtx = document.getElementById('dailyStepsChart').getContext('2d');
    new Chart(dailyStepsCtx, {
        type: 'bar',  // Use bar chart for daily steps
        data: {
            labels: dates,
            datasets: [{
                label: 'Daily Steps',
                data: stepsData,
                backgroundColor: '#2196F3'
            }]
        }
    });
}

// Call fetchData to load charts when the page loads
window.onload = fetchData;
