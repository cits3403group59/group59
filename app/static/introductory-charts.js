// filepath: /home/oliviafitzgerald/cits3403/GroupProject/group59/app/static/introductory-charts.js

// Doughnut Chart
function createDoughnutChart() {
  const donutCtx = document.getElementById('twin-data').getContext('2d');
  new Chart(donutCtx, {
      type: 'doughnut',
      data: {
          datasets: [{
              data: [85, 15], // 85% filled, 15% empty
              backgroundColor: ['#FA3980', '#ffffff'],
              borderColor: ['#FA3980', '#ffffff'],
              borderWidth: 1
          }]
      },
      options: {
          responsive: true,
          cutout: '70%',
          plugins: {
              tooltip: {
                  callbacks: {
                      label: function(tooltipItem) {
                          const label = tooltipItem.label || '';
                          const value = tooltipItem.raw || 0;
                          return `${label}: ${value}%`;
                      }
                  }
              }
          }
      },
      plugins: [
          {
              id: 'centerLabel',
              beforeDraw: function(chart) {
                  const { width } = chart;
                  const { height } = chart;
                  const ctx = chart.ctx;

                  ctx.save();
                  ctx.font = 'bold 80px Arial';
                  ctx.fillStyle = '#FA3980';
                  ctx.textAlign = 'center';
                  ctx.textBaseline = 'middle';
                  ctx.fillText('85%', width / 2, height / 2); // Centered text for percentage
                  ctx.restore();
              }
          }
      ]
  });
}

// Bar Chart
function createBarChart() {
  const barCtx = document.getElementById('sleep-data').getContext('2d');
  new Chart(barCtx, {
      type: 'bar',
      data: {
          labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
          datasets: [{
              label: 'You',
              data: [8.5, 7, 8, 7, 10, 10, 9.5],
              backgroundColor: '#FA3980',
              borderColor: '#FA3980',
              borderWidth: 1
          }, {
              label: 'Your Twin',
              data: [9, 9, 7, 8, 9, 10, 9.5],
              backgroundColor: '#ffffff',
              borderColor: '#ffffff',
              borderWidth: 1
          }]
      },
      options: {
          responsive: true,
          plugins: {
              title: {
                  display: true,
                  text: 'Sleep Habit Comparison', 
                  font: {
                      size: 20,
                      family: 'Arial',
                      weight: 'bold'
                  },
                  color: '#000000',
              },
              legend: {
                  labels: {
                      color: '#000000' // Change legend label color
                  }
              }
          },
          scales: {
              x: {
                  stacked: false, // Ensure grouped bars
                  ticks: {
                      color: '#000000' // Change x-axis label color
                  },
                  title: {
                    display: true,
                    text: 'Day of the Week', // X-axis label
                    font: {
                        size: 14,
                        family: 'Arial',
                        weight: 'bold'
                    },
                    color: '#000000'
                }
              },
              y: {
                  beginAtZero: true,
                  ticks: {
                      color: '#000000', // Change y-axis label color
                  },
                  title: {
                      display: true,
                      text: 'Hours of Sleep', // Y-axis label
                      font: {
                          size: 14,
                          family: 'Arial',
                          weight: 'bold'
                      },
                      color: '#000000'
                  }
              }
          }
      }
  });
}

function createStackedBarChart() {
  const socialMediaCtx = document.getElementById('social-media-data').getContext('2d');
  new Chart(socialMediaCtx, {
      type: 'bar',
      data: {
          labels: ['You', 'Your Twin'], // Each bar represents a person
          datasets: [{
              label: 'Facebook',
              data: [30, 20], // Example percentages for each person
              backgroundColor: '#FA3980',
              borderColor: '#FA3980',
              borderWidth: 1
          }, {
              label: 'Instagram',
              data: [25, 30],
              backgroundColor: '#FF6384',
              borderColor: '#FF6384',
              borderWidth: 1
          }, {
              label: 'Twitter',
              data: [20, 25],
              backgroundColor: '#FFCDD3',
              borderColor: '#FFCDD3',
              borderWidth: 1
          }, {
              label: 'Snapchat',
              data: [15, 10],
              backgroundColor: '#FFB6C1',
              borderColor: '#FFB6C1',
              borderWidth: 1
          }, {
              label: 'TikTok',
              data: [10, 15],
              backgroundColor: '#FF007F',
              borderColor: '#FF007F',
              borderWidth: 1
          }]
      },
      options: {
          responsive: true,
          plugins: {
              title: {
                  display: true,
                  text: 'Social Media Usage Comparison',
                  font: {
                      size: 20,
                      family: 'Arial',
                      weight: 'bold'
                  },
                  color: '#000000',
              },
              legend: {
                  labels: {
                      color: '#000000' // Change legend label color
                  }
              }
          },
          scales: {
              x: {
                  stacked: true, // Enable stacked bars
                  ticks: {
                      color: '#000000' // Change x-axis label color
                  }
              },
              y: {
                  stacked: true, // Enable stacked bars
                  beginAtZero: true,
                  ticks: {
                      color: '#000000', // Change y-axis label color
                      callback: function(value) {
                          return value + '%'; // Append % to y-axis labels
                      }
                  },
                  title: {
                    display: true,
                    text: 'Proportion of Total Screen Time', // Y-axis label
                    font: {
                        size: 14,
                        family: 'Arial',
                        weight: 'bold'
                    },
                    color: '#000000'
                }
              }
          }
      }
  });
}

// Call the function to create the stacked bar chart
// Ensure both charts are created after the DOM has fully loaded
document.addEventListener('DOMContentLoaded', () => {
  createDoughnutChart();
  createBarChart();
  createStackedBarChart();
});