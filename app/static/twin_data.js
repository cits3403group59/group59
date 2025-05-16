// Update the HTML content with fetched twin comparison data
function updateTwinComparison(data) {
    const keys = Object.keys(data); // Get all keys ('sleep', 'coffee', etc.)
    keys.forEach(key => {
        const entry = data[key];
        if (!entry) return;

        document.getElementById(`${key}-you`).textContent = entry.you; // Update the 'You' value
        document.getElementById(`${key}-twin`).textContent = entry.twin; // Update the 'Twin' value
        document.getElementById(`${key}-match`).textContent = `${entry.match}%`; // Update the 'Match' %
    });
}

// Fetch twin data from backend API
async function fetchTwinData() {
    try {
        const res = await fetch(`/api/twin-comparison`);
        if (!res.ok) throw new Error('Failed to fetch twin comparison.');
        const data = await res.json(); // JSON contains all of the feature matches
        updateTwinComparison(data); // Render in UI
    } catch (e) {
        console.error('Twin fetch error:', e); // Log any errors
    }
}

document.addEventListener('DOMContentLoaded', fetchTwinData);
