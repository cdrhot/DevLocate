/**
 * DevLocate - Frontend JS
 * Find K nearest people near you
 */

class MapApplication {
    constructor() {
        // Map elements
        this.map = null;
        this.userMarkers = [];
        this.currentLocationMarker = null;
        
        // Nearby users form elements
        this.nearbyUsersForm = document.getElementById('nearbyUsersForm');
        this.currentLatInput = document.getElementById('currentLat');
        this.currentLonInput = document.getElementById('currentLon');
        this.kValueInput = document.getElementById('kValue');
        this.geoLocationBtn = document.getElementById('geoLocationBtn');
        
        // Users result elements
        this.usersResults = document.getElementById('usersResults');
        this.usersList = document.getElementById('usersList');
        
        // Common elements
        this.errorDiv = document.getElementById('errorMessage');
        this.loadingDiv = document.getElementById('loadingIndicator');
        
        // Initialize app
        this.init();
    }
    
    /**
     * Initialize the application
     */
    init() {
        this.initializeMap();
        this.attachEventListeners();
    }
    
    /**
     * Initialize Leaflet map
     */
    initializeMap() {
        // Create map centered on NYC
        this.map = L.map('map').setView([40.7128, -74.0060], 13);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19,
            minZoom: 2
        }).addTo(this.map);
    }
    
    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // Nearby users form submission
        this.nearbyUsersForm.addEventListener('submit', (e) => this.handleNearbyUsersFormSubmit(e));
        
        // Geolocation button
        this.geoLocationBtn.addEventListener('click', () => this.requestGeolocation());
    }
    
    /**
     * Request geolocation permission
     */
    requestGeolocation() {
        if (!navigator.geolocation) {
            this.showError('Geolocation is not supported by your browser');
            return;
        }
        
        this.showLoading(true);
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                this.currentLatInput.value = position.coords.latitude.toFixed(4);
                this.currentLonInput.value = position.coords.longitude.toFixed(4);
                this.showLoading(false);
                this.hideError();
            },
            (error) => {
                this.showLoading(false);
                this.showError(`Geolocation error: ${error.message}`);
            }
        );
    }
    
    /**
     * Handle nearby users form submission
     */
    async handleNearbyUsersFormSubmit(e) {
        e.preventDefault();
        await this.fetchAndDisplayNearbyUsers();
    }
    
    /**
     * Fetch nearby users from backend API
     */
    async fetchAndDisplayNearbyUsers() {
        // Get input values
        const currentLat = parseFloat(this.currentLatInput.value);
        const currentLon = parseFloat(this.currentLonInput.value);
        const k = parseInt(this.kValueInput.value) || 5;
        
        // Validate inputs
        if (!this.validateCoordinates(currentLat, currentLon, currentLat, currentLon)) {
            this.showError('Please enter valid coordinates (lat: -90 to 90, lon: -180 to 180)');
            return;
        }
        
        if (k < 1 || k > 15) {
            this.showError('K must be between 1 and 15');
            return;
        }
        
        // Show loading indicator
        this.showLoading(true);
        this.hideError();
        this.hideUsersResults();
        
        try {
            // Build API URL
            const url = new URL('/api/users/nearby', window.location.origin);
            url.searchParams.append('latitude', currentLat);
            url.searchParams.append('longitude', currentLon);
            url.searchParams.append('k', k);
            
            // Fetch nearby users
            const response = await fetch(url);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to fetch nearby users');
            }
            
            const usersData = await response.json();
            
            // Display users on map
            this.displayNearbyUsers(usersData);
            
            // Show results
            this.showUsersResults(usersData);
            
        } catch (error) {
            console.error('Error:', error);
            this.showError(error.message || 'Failed to fetch nearby users');
        } finally {
            this.showLoading(false);
        }
    }
    
    /**
     * Display nearby users on map
     */
    displayNearbyUsers(usersData) {
        // Clear previous markers
        this.clearAllMarkers();
        
        const users = usersData.users || [];
        const currentLat = usersData.current_location.latitude;
        const currentLon = usersData.current_location.longitude;
        const colors = ['#3498db', '#9b59b6', '#e67e22', '#1abc9c', '#f39c12', '#2ecc71', '#e74c3c'];
        
        // Add current location marker (blue)
        this.currentLocationMarker = L.circleMarker(
            [currentLat, currentLon],
            {
                radius: 8,
                fillColor: '#2ecc71',
                color: '#229954',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.8
            }
        ).addTo(this.map)
        .bindPopup('<b>You are here</b>');
        
        // Add user markers
        users.forEach((user, index) => {
            const color = colors[index % colors.length];
            
            const marker = L.circleMarker(
                [user.latitude, user.longitude],
                {
                    radius: 6,
                    fillColor: color,
                    color: color,
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.7
                }
            ).addTo(this.map)
            .bindPopup(`<b>${user.username}</b><br>Distance: ${user.distance_km} km`);
            
            this.userMarkers.push(marker);
        });
        
        // Fit map to show current location and all users
        const allMarkers = [this.currentLocationMarker, ...this.userMarkers].filter(Boolean);
        if (allMarkers.length > 0) {
            const group = new L.featureGroup(allMarkers);
            this.map.fitBounds(group.getBounds().pad(0.1));
        }
    }
    
    /**
     * Clear all markers from map
     */
    clearAllMarkers() {
        // Clear user markers
        this.userMarkers.forEach(marker => {
            this.map.removeLayer(marker);
        });
        this.userMarkers = [];
        
        // Clear current location marker
        if (this.currentLocationMarker) {
            this.map.removeLayer(this.currentLocationMarker);
            this.currentLocationMarker = null;
        }
    }
    
    /**
     * Show users results in sidebar
     */
    showUsersResults(usersData) {
        const users = usersData.users || [];
        const currentLat = usersData.current_location.latitude;
        const currentLon = usersData.current_location.longitude;
        
        // Clear previous list
        this.usersList.innerHTML = '';
        
        if (users.length === 0) {
            this.usersList.innerHTML = '<p style="color: #7f8c8d; font-size: 12px;">No people found nearby.</p>';
            this.usersResults.classList.remove('hidden');
            return;
        }
        
        // Add users to list
        users.forEach((user, index) => {
            const userElement = document.createElement('div');
            userElement.className = 'user-item';
            userElement.style.cursor = 'pointer';
            userElement.innerHTML = `
                <div class="user-item-header">
                    <span class="user-name">#${index + 1} ${user.username}</span>
                    <span class="user-distance">${user.distance_km} km</span>
                </div>
                <div class="user-coords">
                    📍 ${user.latitude.toFixed(4)}, ${user.longitude.toFixed(4)}
                </div>
                <div style="margin-top: 5px; color: #3498db; font-size: 11px; font-weight: 600;">
                    👆 Click to show route
                </div>
            `;
            
            // Add click handler to show directions to this user
            userElement.addEventListener('click', () => {
                this.showDirectionToUser(
                    currentLat,
                    currentLon,
                    user.latitude,
                    user.longitude,
                    user.username
                );
            });
            
            this.usersList.appendChild(userElement);
        });
        
        this.usersResults.classList.remove('hidden');
    }
    
    /**
     * Hide users results
     */
    hideUsersResults() {
        this.usersResults.classList.add('hidden');
    }
    
    /**
     * Show error message
     */
    showError(message) {
        this.errorDiv.textContent = message;
        this.errorDiv.classList.remove('hidden');
        
        // Check if it's a success message (starts with ✅)
        if (message.startsWith('✅')) {
            this.errorDiv.classList.add('success');
        } else {
            this.errorDiv.classList.remove('success');
        }
    }
    
    /**
     * Hide error message
     */
    hideError() {
        this.errorDiv.classList.add('hidden');
        this.errorDiv.classList.remove('success');
    }
    
    /**
     * Show/hide loading indicator
     */
    showLoading(show) {
        if (show) {
            this.loadingDiv.classList.remove('hidden');
        } else {
            this.loadingDiv.classList.add('hidden');
        }
    }
    
    /**
     * Validate coordinates
     */
    validateCoordinates(lat1, lon1, lat2, lon2) {
        return (
            -90 <= lat1 && lat1 <= 90 &&
            -180 <= lon1 && lon1 <= 180 &&
            -90 <= lat2 && lat2 <= 90 &&
            -180 <= lon2 && lon2 <= 180
        );
    }
    
    /**
     * Show direction/route to a specific user
     */
    async showDirectionToUser(originLat, originLon, destLat, destLon, userName) {
        // Show loading
        this.showLoading(true);
        this.hideError();
        
        try {
            // Build API URL for OSRM route
            const url = new URL('/api/osm/route', window.location.origin);
            url.searchParams.append('origin_lat', originLat);
            url.searchParams.append('origin_lon', originLon);
            url.searchParams.append('destination_lat', destLat);
            url.searchParams.append('destination_lon', destLon);
            
            // Fetch route
            const response = await fetch(url);
            
            if (!response.ok) {
                // If route endpoint doesn't exist, just draw a line between points
                const coordinates = [[originLat, originLon], [destLat, destLon]];
                const routeLayer = L.polyline(
                    coordinates,
                    {
                        color: '#3498db',
                        weight: 4,
                        opacity: 0.8,
                        lineCap: 'round',
                        lineJoin: 'round'
                    }
                ).addTo(this.map);
                
                // Calculate straight-line distance
                const distance = this.calculateDistance(originLat, originLon, destLat, destLon);
                this.showError(`✅ Route to ${userName} - ~${distance.toFixed(2)} km`);
                
                // Fit map to show both points
                const group = new L.featureGroup([
                    L.circleMarker([originLat, originLon]),
                    L.circleMarker([destLat, destLon])
                ]);
                this.map.fitBounds(group.getBounds().pad(0.1));
                
                this.showLoading(false);
                return;
            }
            
            const routeData = await response.json();
            
            // Add route line to map (blue)
            if (routeData.geometry && routeData.geometry.coordinates) {
                const coordinates = routeData.geometry.coordinates.map(coord => [coord[1], coord[0]]);
                
                const routeLayer = L.polyline(
                    coordinates,
                    {
                        color: '#3498db',
                        weight: 4,
                        opacity: 0.8,
                        lineCap: 'round',
                        lineJoin: 'round'
                    }
                ).addTo(this.map);
            }
            
            // Show success message
            this.showError(`✅ Route to ${userName} - ${routeData.distance_km} km (${routeData.duration_minutes} min)`);
            
        } catch (error) {
            console.error('Error:', error);
            this.showError(error.message || 'Failed to fetch route to user');
        } finally {
            this.showLoading(false);
        }
    }
    
    /**
     * Calculate distance between two coordinates using Haversine formula
     */
    calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Earth's radius in km
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                  Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                  Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new MapApplication();
});
