// API Configuration
const API_URL = 'http://localhost:8000';
const API_BASE = `${API_URL}/api/v1`;

// DOM Elements
const startLocationInput = document.getElementById('startLocation');
const endLocationInput = document.getElementById('endLocation');
const calculateBtn = document.getElementById('calculateBtn');
const resultSection = document.getElementById('resultSection');
const errorSection = document.getElementById('errorSection');
const loadingSection = document.getElementById('loadingSection');
const graphInfoDiv = document.getElementById('graphInfo');

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  checkServerStatus();
  loadGraphInfo();
  calculateBtn.addEventListener('click', calculateRoute);
});

// Check if server is online
async function checkServerStatus() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    if (response.ok) {
      document.getElementById('serverStatus').textContent = 'Live';
      document.querySelector('.status-dot').style.background = '#4ade80';
    }
  } catch (error) {
    document.getElementById('serverStatus').textContent = 'Offline';
    document.querySelector('.status-dot').style.background = '#ff6464';
  }
}

// Load graph information
async function loadGraphInfo() {
  try {
    const response = await fetch(`${API_BASE}/graph`);
    const data = await response.json();
    graphInfoDiv.innerHTML = `
      <p><strong>Available Locations:</strong> ${data.total_nodes}</p>
      <p><strong>Network Connections:</strong> ${data.total_edges}</p>
      <p><strong>Network Nodes:</strong> ${data.nodes.join(', ')}</p>
    `;
  } catch (error) {
    graphInfoDiv.innerHTML = '<p style="color: red;">Failed to load network info</p>';
  }
}

// Calculate route
async function calculateRoute() {
  const start = startLocationInput.value.trim();
  const end = endLocationInput.value.trim();
  
  // Validation
  if (!start || !end) {
    showError('Please enter both start and destination locations');
    return;
  }
  
  if (start === end) {
    showError('Start and destination must be different');
    return;
  }
  
  // Show loading state
  hideError();
  resultSection.style.display = 'none';
  loadingSection.style.display = 'block';
  calculateBtn.disabled = true;
  calculateBtn.classList.add('loading');
  
  try {
    const response = await fetch(`${API_BASE}/route`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ start, end })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to calculate route');
    }
    
    const data = await response.json();
    
    // Display results
    displayResults(data);
    loadingSection.style.display = 'none';
    resultSection.style.display = 'block';
    
  } catch (error) {
    showError(error.message || 'An error occurred');
    loadingSection.style.display = 'none';
  } finally {
    calculateBtn.disabled = false;
    calculateBtn.classList.remove('loading');
  }
}

// Display results
function displayResults(data) {
  document.getElementById('totalDistance').textContent = data.distance + ' km';
  document.getElementById('totalStops').textContent = data.path.length;
  document.getElementById('nodesExplored').textContent = data.nodes_visited;
  
  // Display path with animation
  const pathList = document.getElementById('pathList');
  pathList.innerHTML = '';
  
  data.path.forEach((location, index) => {
    const item = document.createElement('span');
    item.className = 'path-item';
    item.textContent = location;
    item.style.animationDelay = `${index * 0.1}s`;
    pathList.appendChild(item);
    
    if (index < data.path.length - 1) {
      const arrow = document.createElement('span');
      arrow.className = 'path-arrow';
      arrow.textContent = ' → ';
      pathList.appendChild(arrow);
    }
  });
}

// Show error message
function showError(message) {
  document.getElementById('errorMessage').textContent = message;
  errorSection.style.display = 'block';
  resultSection.style.display = 'none';
}

// Hide error message
function hideError() {
  errorSection.style.display = 'none';
}

// Reset form
function resetForm() {
  startLocationInput.value = '';
  endLocationInput.value = '';
  resultSection.style.display = 'none';
  errorSection.style.display = 'none';
  startLocationInput.focus();
}
