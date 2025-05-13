// Fetch data from your Flask API using the get_data_between route
async function fetchData() {
  console.log(userId);
  const startDate = document.getElementById("startDate").value;  // Assuming you have a date range input
  const endDate = document.getElementById("endDate").value;
  const url = `/api/userdata/${userId}?start=${startDate}&end=${endDate}`;

  if (!startDate || !endDate) {
    console.log("Please enter both start and end dates.");
    return;  // Prevent fetching if either date is missing
  }

  try {
    const response = await fetch(url);
    const data = await response.json();
    renderCharts(data);  // Once data is fetched, render the charts
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

// Add event listeners to the start and end date fields
document.getElementById("startDate").addEventListener('change', fetchData);
document.getElementById("endDate").addEventListener('change', fetchData);

// Render the charts using Chart.js
function renderCharts(data) {
  // Prepare data for the charts
  const dates = data.map(d => d.date);
  const sleepData = data.map(d => d.sleep_hours);
  const coffeeData = data.map(d => d.coffee_intake);
  const stepsData = data.map(d => d.daily_steps);
  const alcoholData = data.map(d => d.alcohol);
  const bedTimeData = data.map(d => d.bed_time);
  const exerciseData = data.map(d => d.exercise_minutes);
  const moneyData = data.map(d => d.money_spent);
  const moodData = data.map(d => d.mood);
  const screenTimeData = data.map(d => d.screen_time);
  const socialMediaData = data.map(d => d.social_media);
  const socialTimeData = data.map(d => d.social_time);
  const studyTimeData = data.map(d => d.study_time);
  const transportationData = data.map(d => d.transportation);
  const wakeUpTimeData = data.map(d => d.wake_up_time);
  const workTimeData = data.map(d => d.work_time);

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

  // Chart for Alcohol Consumption
  const alcoholCtx = document.getElementById('alcoholChart').getContext('2d');
  new Chart(alcoholCtx, {
    type: 'bar',  // Use bar chart for alcohol consumption
    data: {
      labels: dates,
      datasets: [{
        label: 'Alcohol Consumption (Units)',
        data: alcoholData,
        backgroundColor: '#F44336'
      }]
    }
  });
  // Chart for Bed Time
  const bedTimeCtx = document.getElementById('bedTimeChart').getContext('2d');
  new Chart(bedTimeCtx, {
    type: 'bar',  // Use line chart for bed time
    data: {
      labels: dates,
      datasets: [{
        label: 'Bed Time',
        data: bedTimeData,
        borderColor: '#9C27B0',
        fill: false
      }]
    }
  });
  // Chart for Exercise Minutes
  const exerciseCtx = document.getElementById('exerciseChart').getContext('2d');
  new Chart(exerciseCtx, {
    type: 'line',  // Use bar chart for exercise minutes
    data: {
      labels: dates,
      datasets: [{
        label: 'Exercise Minutes',
        data: exerciseData,
        backgroundColor: '#3F51B5'
      }]
    }
  });
  // Chart for Money Spent
  const moneyCtx = document.getElementById('moneyChart').getContext('2d');
  new Chart(moneyCtx, {
    type: 'bar',  // Use bar chart for money spent
    data: {
      labels: dates,
      datasets: [{
        label: 'Money Spent ($)',
        data: moneyData,
        backgroundColor: '#FF5722'
      }]
    }
  });
  // Chart for Mood
  const moodCtx = document.getElementById('moodChart').getContext('2d');
  new Chart(moodCtx, {
    type: 'line',  // Use line chart for mood
    data: {
      labels: dates,
      datasets: [{
        label: 'Mood',
        data: moodData,
        borderColor: '#E91E63',
        fill: false
      }]
    }
  });
  // Chart for Screen Time
  const screenTimeCtx = document.getElementById('screenTimeChart').getContext('2d');
  new Chart(screenTimeCtx, {
    type: 'bar',  // Use bar chart for screen time
    data: {
      labels: dates,
      datasets: [{
        label: 'Screen Time (Hours)',
        data: screenTimeData,
        backgroundColor: '#009688'
      }]
    }
  });
  // Chart for Social Media Usage
  const socialMediaCtx = document.getElementById('socialMediaChart').getContext('2d');
  new Chart(socialMediaCtx, {
    type: 'bar',  // Use bar chart for social media usage
    data: {
      labels: dates,
      datasets: [{
        label: 'Social Media Usage (Hours)',
        data: socialMediaData,
        backgroundColor: '#8BC34A'
      }]
    }
  });
  // Chart for Social Time
  const socialTimeCtx = document.getElementById('socialTimeChart').getContext('2d');
  new Chart(socialTimeCtx, {
    type: 'bar',  // Use bar chart for social time
    data: {
      labels: dates,
      datasets: [{
        label: 'Social Time (Hours)',
        data: socialTimeData,
        backgroundColor: '#CDDC39'
      }]
    }
  });
  // Chart for Study Time
  const studyTimeCtx = document.getElementById('studyTimeChart').getContext('2d');
  new Chart(studyTimeCtx, {
    type: 'bar',  // Use bar chart for study time
    data: {
      labels: dates,
      datasets: [{
        label: 'Study Time (Hours)',
        data: studyTimeData,
        backgroundColor: '#FFEB3B'
      }]
    }
  });
  // Chart for Transportation
  const transportationCtx = document.getElementById('transportationChart').getContext('2d');
  new Chart(transportationCtx, {
    type: 'bar',  // Use bar chart for transportation
    data: {
      labels: dates,
      datasets: [{
        label: 'Transportation (Hours)',
        data: transportationData,
        backgroundColor: '#FFC107'
      }]
    }
  });
  // Chart for Wake Up Time
  const wakeUpTimeCtx = document.getElementById('wakeUpTimeChart').getContext('2d');
  new Chart(wakeUpTimeCtx, {
    type: 'line',  // Use line chart for wake up time
    data: {
      labels: dates,
      datasets: [{
        label: 'Wake Up Time',
        data: wakeUpTimeData,
        borderColor: '#FF9800',
        fill: false
      }]
    }
  });
  // Chart for Work Time
  const workTimeCtx = document.getElementById('workTimeChart').getContext('2d');
  new Chart(workTimeCtx, {
    type: 'bar',  // Use bar chart for work time
    data: {
      labels: dates,
      datasets: [{
        label: 'Work Time (Hours)',
        data: workTimeData,
        backgroundColor: '#FF5722'
      }]
    }
  });
}
