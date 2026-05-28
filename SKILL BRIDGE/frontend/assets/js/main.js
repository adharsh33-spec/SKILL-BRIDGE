/* SkillBridge Main JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize navigation smooth scroll
    const navLinks = document.querySelectorAll('.navbar-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                if (targetId === '#home') {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            }
        });
    });
});

// Utility function to check authentication
function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

// Utility function to get stored user
function getStoredUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

// Utility function to get auth token
function getAuthToken() {
    return localStorage.getItem('token');
}

// Utility function to make API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (getAuthToken()) {
        options.headers['Authorization'] = `Bearer ${getAuthToken()}`;
    }

    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(endpoint, options);
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        return { status: 'error', message: error.message };
    }
}

// Redirect to login if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/frontend/pages/login.html';
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/frontend/index.html';
}

// Initialize with console message
console.log('SkillBridge Application Loaded');
