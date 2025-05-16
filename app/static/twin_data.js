// Fetch twin comparison data
async function fetchTwinData() {
    try {
        const response = await fetch(`/api/twin-comparison/${userId}`);
        const data = await response.json();
        updateTwinComparison(data);
    } catch (error) {
        console.error('Error fetching twin data:', error);
    }
}

// Update DOM with twin comparison data
function updateTwinComparison(data) {
    // Sleep data
    document.getElementById('sleep-you').textContent = data.sleep.you;
    document.getElementById('sleep-twin').textContent = data.sleep.twin;
    document.getElementById('sleep-match').textContent = `${data.sleep.match}%`;
    document.getElementById('sleep-diff').textContent = formatDifference(data.sleep.difference, 'h');
    
    // Coffee data
    document.getElementById('coffee-you').textContent = data.coffee.you;
    document.getElementById('coffee-twin').textContent = data.coffee.twin;
    document.getElementById('coffee-match').textContent = `${data.coffee.match}%`;
    document.getElementById('coffee-diff').textContent = formatDifference(data.coffee.difference, '');
    
    // Steps data
    document.getElementById('steps-you').textContent = data.steps.you.toLocaleString();
    document.getElementById('steps-twin').textContent = data.steps.twin.toLocaleString();
    document.getElementById('steps-match').textContent = `${data.steps.match}%`;
    document.getElementById('steps-diff').textContent = formatDifference(data.steps.difference, 'steps');
    
    // Time data
    document.getElementById('wakeup-you').textContent = formatTime(data.wakeup.you);
    document.getElementById('wakeup-twin').textContent = formatTime(data.wakeup.twin);
    document.getElementById('wakeup-match').textContent = `${data.wakeup.match}%`;
    document.getElementById('wakeup-diff').textContent = formatTimeDifference(data.wakeup.difference);
    
    document.getElementById('bed-you').textContent = formatTime(data.bed.you);
    document.getElementById('bed-twin').textContent = formatTime(data.bed.twin);
    document.getElementById('bed-match').textContent = `${data.bed.match}%`;
    document.getElementById('bed-diff').textContent = formatTimeDifference(data.bed.difference);
}

// Helper functions
function formatDifference(value, unit) {
    if (value > 0) {
        return `+${Math.abs(value)}${unit}`;
    } else if (value < 0) {
        return `-${Math.abs(value)}${unit}`;
    }
    return `Same ${unit}`;
}

function formatTime(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}`;
}

function formatTimeDifference(diffMinutes) {
    const absDiff = Math.abs(diffMinutes);
    const hours = Math.floor(absDiff / 60);
    const mins = absDiff % 60;
    
    let timeStr = '';
    if (hours > 0) timeStr += `${hours}h `;
    if (mins > 0) timeStr += `${mins}m`;
    
    if (diffMinutes > 0) {
        return `+${timeStr} earlier`;
    } else if (diffMinutes < 0) {
        return `-${timeStr} later`;
    }
    return 'Same time';
}

// Initialise
document.addEventListener('DOMContentLoaded', fetchTwinData);