// SheSafe - Frontend JavaScript

const API_BASE = 'http://localhost:5000/api';
let currentLocation = null;

// Navigation
document.addEventListener('DOMContentLoaded', function() {
    // Setup navigation
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.dataset.section;
            navigateToSection(section);
        });
    });
    
    // Setup quick SOS
    const quickSOSBtn = document.getElementById('quickSOS');
    if (quickSOSBtn) {
        quickSOSBtn.addEventListener('click', sendQuickSOS);
    }
    
    // Load emergency contacts
    loadContacts();
    
    // Check system health
    checkSystemHealth();
});

function navigateToSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Show selected section
    const section = document.getElementById(sectionName);
    if (section) {
        section.classList.add('active');
    }
    
    // Activate nav link
    const navLink = document.querySelector(`[data-section="${sectionName}"]`);
    if (navLink) {
        navLink.classList.add('active');
    }
}

// Loading overlay
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// Toxicity Detection
async function analyzeToxicity() {
    const text = document.getElementById('toxicityText').value.trim();
    
    if (!text) {
        alert('Please enter text to analyze');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/toxicity/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        displayToxicityResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Error analyzing text. Please try again.');
    } finally {
        hideLoading();
    }
}

function displayToxicityResults(data) {
    const resultsDiv = document.getElementById('toxicityResults');
    const contentDiv = document.getElementById('toxicityContent');
    
    if (data.error) {
        contentDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        resultsDiv.style.display = 'block';
        return;
    }
    
    const riskClass = `risk-${data.risk_level.toLowerCase()}`;
    
    let html = `
        <div class="risk-badge ${riskClass}">${data.risk_level} RISK</div>
        <p><strong>Is Toxic:</strong> ${data.is_toxic ? 'Yes ⚠️' : 'No ✅'}</p>
        <p><strong>Maximum Score:</strong> ${(data.max_score * 100).toFixed(1)}%</p>
        <h4>Detailed Scores:</h4>
    `;
    
    for (const [key, value] of Object.entries(data.scores)) {
        const percentage = (value * 100).toFixed(1);
        const color = value > 0.7 ? '#f44336' : value > 0.4 ? '#ff9800' : '#4caf50';
        html += `
            <div class="score-item">
                <span>${key.replace(/_/g, ' ').toUpperCase()}</span>
                <strong>${percentage}%</strong>
            </div>
            <div class="score-bar">
                <div class="score-fill" style="width: ${percentage}%; background: ${color};">
                    ${percentage}%
                </div>
            </div>
        `;
    }
    
    contentDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
}

async function analyzeConversation() {
    const text = document.getElementById('conversationText').value.trim();
    
    if (!text) {
        alert('Please enter messages to analyze');
        return;
    }
    
    const messages = text.split('\n').filter(msg => msg.trim());
    
    if (messages.length < 2) {
        alert('Please enter at least 2 messages');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/toxicity/analyze-conversation`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages })
        });
        
        const data = await response.json();
        displayConversationResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Error analyzing conversation. Please try again.');
    } finally {
        hideLoading();
    }
}

function displayConversationResults(data) {
    const resultsDiv = document.getElementById('conversationResults');
    const contentDiv = document.getElementById('conversationContent');
    
    if (data.error) {
        contentDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        resultsDiv.style.display = 'block';
        return;
    }
    
    const riskClass = `risk-${data.overall_risk_level.toLowerCase()}`;
    
    let html = `
        <div class="risk-badge ${riskClass}">${data.overall_risk_level} RISK</div>
        <p><strong>Total Messages:</strong> ${data.message_count}</p>
        <p><strong>Toxic Messages:</strong> ${data.toxic_message_count} (${data.toxicity_percentage.toFixed(1)}%)</p>
        <h4>Average Scores:</h4>
    `;
    
    for (const [key, value] of Object.entries(data.average_scores)) {
        const percentage = (value * 100).toFixed(1);
        html += `
            <div class="score-item">
                <span>${key.replace(/_/g, ' ').toUpperCase()}</span>
                <strong>${percentage}%</strong>
            </div>
        `;
    }
    
    contentDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
}

// Emotion Detection
async function analyzeEmotion() {
    const text = document.getElementById('emotionText').value.trim();
    
    if (!text) {
        alert('Please enter text to analyze');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/emotion/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        displayEmotionResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Error analyzing emotions. Please try again.');
    } finally {
        hideLoading();
    }
}

function displayEmotionResults(data) {
    const resultsDiv = document.getElementById('emotionResults');
    const contentDiv = document.getElementById('emotionContent');
    
    if (data.error) {
        contentDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        resultsDiv.style.display = 'block';
        return;
    }
    
    const riskClass = `risk-${data.mental_health_risk.level.toLowerCase()}`;
    
    let html = `
        <div class="risk-badge ${riskClass}">Mental Health Risk: ${data.mental_health_risk.level}</div>
        <p><strong>Dominant Emotion:</strong> ${data.dominant_emotion.name.toUpperCase()} 
           (${(data.dominant_emotion.score * 100).toFixed(1)}%)</p>
        <p><strong>Sentiment:</strong> ${data.sentiment.label} (${(data.sentiment.score * 100).toFixed(1)}%)</p>
        ${data.needs_support ? '<p class="warning"><strong>⚠️ Support may be needed</strong></p>' : ''}
        <h4>Emotion Breakdown:</h4>
    `;
    
    for (const [emotion, score] of Object.entries(data.emotions)) {
        const percentage = (score * 100).toFixed(1);
        const color = ['sadness', 'fear', 'anger'].includes(emotion) && score > 0.6 ? '#f44336' : '#4caf50';
        html += `
            <div class="score-item">
                <span>${emotion.toUpperCase()}</span>
                <strong>${percentage}%</strong>
            </div>
            <div class="score-bar">
                <div class="score-fill" style="width: ${percentage}%; background: ${color};">
                    ${percentage}%
                </div>
            </div>
        `;
    }
    
    contentDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
}

// Safety Scoring
function getCurrentLocation() {
    if (navigator.geolocation) {
        showLoading();
        navigator.geolocation.getCurrentPosition(
            (position) => {
                currentLocation = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                document.getElementById('safetyLat').value = currentLocation.latitude;
                document.getElementById('safetyLng').value = currentLocation.longitude;
                hideLoading();
                alert('Location obtained successfully!');
            },
            (error) => {
                hideLoading();
                alert('Unable to get location: ' + error.message);
            }
        );
    } else {
        alert('Geolocation is not supported by your browser');
    }
}

async function getSafetyScore() {
    const latitude = parseFloat(document.getElementById('safetyLat').value);
    const longitude = parseFloat(document.getElementById('safetyLng').value);
    
    if (isNaN(latitude) || isNaN(longitude)) {
        alert('Please enter valid coordinates or use current location');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/safety/score`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude, longitude })
        });
        
        const data = await response.json();
        displaySafetyResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Error getting safety score. Please try again.');
    } finally {
        hideLoading();
    }
}

function displaySafetyResults(data) {
    const resultsDiv = document.getElementById('safetyResults');
    const contentDiv = document.getElementById('safetyContent');
    
    if (data.error) {
        contentDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        resultsDiv.style.display = 'block';
        return;
    }
    
    const safetyClass = data.safety_level === 'SAFE' ? 'risk-low' : 
                       data.safety_level === 'MODERATE' ? 'risk-medium' :
                       data.safety_level === 'CAUTION' ? 'risk-high' : 'risk-critical';
    
    let html = `
        <div class="risk-badge ${safetyClass}">${data.safety_level}</div>
        <p><strong>Location:</strong> ${data.location_name}</p>
        <p><strong>Safety Score:</strong> ${data.safety_score}/100</p>
        <p><strong>Crime Risk:</strong> ${(data.crime_risk * 100).toFixed(1)}%</p>
        <p><strong>Time Risk Factor:</strong> ${data.time_risk_factor.toFixed(2)}x</p>
        
        ${data.nearby_incidents.length > 0 ? `
            <h4>Nearby Incidents:</h4>
            <ul>
                ${data.nearby_incidents.map(inc => 
                    `<li>${inc.type} (${inc.severity}) - ${inc.distance_km} km away</li>`
                ).join('')}
            </ul>
        ` : ''}
        
        <h4>Recommendations:</h4>
        <ul>
            ${data.recommendations.map(rec => `<li>${rec}</li>`).join('')}
        </ul>
    `;
    
    contentDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
}

async function findSafeRoute() {
    const startLat = parseFloat(document.getElementById('startLat').value);
    const startLng = parseFloat(document.getElementById('startLng').value);
    const endLat = parseFloat(document.getElementById('endLat').value);
    const endLng = parseFloat(document.getElementById('endLng').value);
    
    if ([startLat, startLng, endLat, endLng].some(isNaN)) {
        alert('Please enter valid coordinates for both locations');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/safety/route`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                start_latitude: startLat,
                start_longitude: startLng,
                end_latitude: endLat,
                end_longitude: endLng
            })
        });
        
        const data = await response.json();
        displayRouteResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Error finding route. Please try again.');
    } finally {
        hideLoading();
    }
}

function displayRouteResults(data) {
    const resultsDiv = document.getElementById('routeResults');
    const contentDiv = document.getElementById('routeContent');
    
    if (data.error) {
        contentDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        resultsDiv.style.display = 'block';
        return;
    }
    
    const safetyClass = data.overall_route_safety === 'SAFE' ? 'risk-low' : 
                       data.overall_route_safety === 'MODERATE' ? 'risk-medium' :
                       data.overall_route_safety === 'CAUTION' ? 'risk-high' : 'risk-critical';
    
    let html = `
        <div class="risk-badge ${safetyClass}">${data.overall_route_safety}</div>
        <p><strong>Distance:</strong> ${data.distance_km} km</p>
        <p><strong>Average Safety Score:</strong> ${data.average_safety_score}/100</p>
        <p><strong>Minimum Safety Score:</strong> ${data.minimum_safety_score}/100</p>
        
        ${data.warnings.length > 0 ? `
            <h4>⚠️ Warnings:</h4>
            <ul>
                ${data.warnings.map(warning => `<li>${warning}</li>`).join('')}
            </ul>
        ` : '<p>✅ No significant safety concerns detected along this route</p>'}
    `;
    
    contentDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
}

// SOS System
async function sendSOS() {
    const userName = document.getElementById('userName').value.trim() || 'User';
    const message = document.getElementById('sosMessage').value.trim();
    
    if (!currentLocation) {
        // Try to get current location
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    currentLocation = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    };
                    await sendSOSRequest(userName, message);
                },
                (error) => {
                    alert('Location is required for SOS. Please enable location services.');
                }
            );
        } else {
            alert('Geolocation is not supported. Cannot send SOS without location.');
        }
        return;
    }
    
    await sendSOSRequest(userName, message);
}

async function sendSOSRequest(userName, message) {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/sos/alert`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_name: userName,
                latitude: currentLocation.latitude,
                longitude: currentLocation.longitude,
                message: message
            })
        });
        
        const data = await response.json();
        displaySOSResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Error sending SOS. Please try again.');
    } finally {
        hideLoading();
    }
}

async function sendQuickSOS() {
    if (!confirm('Send emergency SOS alert to all contacts?')) {
        return;
    }
    
    const userName = prompt('Your name:', 'User') || 'User';
    
    if (navigator.geolocation) {
        showLoading();
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                currentLocation = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                await sendSOSRequest(userName, 'EMERGENCY ALERT');
            },
            (error) => {
                hideLoading();
                alert('Location is required for SOS. Please enable location services.');
            }
        );
    } else {
        alert('Geolocation is not supported');
    }
}

async function shareLocation() {
    const userName = document.getElementById('shareUserName').value.trim() || 'User';
    
    if (!navigator.geolocation) {
        alert('Geolocation is not supported');
        return;
    }
    
    showLoading();
    navigator.geolocation.getCurrentPosition(
        async (position) => {
            try {
                const response = await fetch(`${API_BASE}/sos/share-location`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_name: userName,
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    })
                });
                
                const data = await response.json();
                displaySOSResults(data);
            } catch (error) {
                console.error('Error:', error);
                alert('Error sharing location. Please try again.');
            } finally {
                hideLoading();
            }
        },
        (error) => {
            hideLoading();
            alert('Unable to get location: ' + error.message);
        }
    );
}

async function sendCheckin() {
    const userName = document.getElementById('checkinName').value.trim() || 'User';
    const status = document.getElementById('checkinStatus').value.trim() || 'Safe';
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/sos/checkin`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_name: userName,
                status: status
            })
        });
        
        const data = await response.json();
        displaySOSResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Error sending check-in. Please try again.');
    } finally {
        hideLoading();
    }
}

function displaySOSResults(data) {
    const resultsDiv = document.getElementById('sosResults');
    const contentDiv = document.getElementById('sosContent');
    
    if (data.error) {
        contentDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        resultsDiv.style.display = 'block';
        return;
    }
    
    let html = `
        <p class="success">✅ ${data.message}</p>
        ${data.location_link ? `<p><strong>Location:</strong> <a href="${data.location_link}" target="_blank">View on Map</a></p>` : ''}
        ${data.timestamp ? `<p><strong>Time:</strong> ${new Date(data.timestamp).toLocaleString()}</p>` : ''}
    `;
    
    if (data.contacts_alerted) {
        html += `<h4>Contacts Alerted:</h4><ul>`;
        data.contacts_alerted.forEach(contact => {
            html += `<li>${contact.contact}: ${contact.status}</li>`;
        });
        html += `</ul>`;
    }
    
    contentDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
}

// Emergency Contacts Management
async function addContact() {
    const phone = document.getElementById('contactPhone').value.trim();
    const name = document.getElementById('contactName').value.trim();
    
    if (!phone) {
        alert('Please enter a phone number');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/sos/contacts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone_number: phone, name: name })
        });
        
        const data = await response.json();
        alert(data.message);
        
        // Clear inputs
        document.getElementById('contactPhone').value = '';
        document.getElementById('contactName').value = '';
        
        // Reload contacts
        loadContacts();
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding contact. Please try again.');
    }
}

async function loadContacts() {
    try {
        const response = await fetch(`${API_BASE}/sos/contacts`);
        const data = await response.json();
        
        const listDiv = document.getElementById('contactsList');
        
        if (data.contacts && data.contacts.length > 0) {
            listDiv.innerHTML = data.contacts.map(contact => `
                <div class="contact-item">
                    <span>${contact}</span>
                    <button class="contact-remove" onclick="removeContact('${contact}')">Remove</button>
                </div>
            `).join('');
        } else {
            listDiv.innerHTML = '<p>No emergency contacts added yet</p>';
        }
    } catch (error) {
        console.error('Error loading contacts:', error);
    }
}

async function removeContact(phone) {
    if (!confirm(`Remove ${phone} from emergency contacts?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/sos/contacts/${encodeURIComponent(phone)}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        alert(data.message);
        loadContacts();
    } catch (error) {
        console.error('Error:', error);
        alert('Error removing contact. Please try again.');
    }
}

// System Health Check
async function checkSystemHealth() {
    try {
        const response = await fetch(`${API_BASE.replace('/api', '')}/api/health`);
        const data = await response.json();
        console.log('System Health:', data);
    } catch (error) {
        console.error('System health check failed:', error);
    }
}

