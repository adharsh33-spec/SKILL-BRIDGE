/* Authentication JavaScript */

// Handle authentication form submission
function handleAuthForm(formType) {
    const form = document.getElementById(`${formType}Form`);
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        // Form submission is handled inline in HTML
    });
}

// Login function
async function login(email, password) {
    const response = await apiCall('/api/auth/login', 'POST', {
        email: email,
        password: password
    });

    if (response.status === 'success') {
        localStorage.setItem('token', response.token);
        localStorage.setItem('user', JSON.stringify(response.user));
        return true;
    }
    return false;
}

// Register function
async function register(email, password, full_name) {
    const response = await apiCall('/api/auth/register', 'POST', {
        email: email,
        password: password,
        full_name: full_name
    });

    return response.status === 'success';
}

// Check if user is already authenticated and redirect
document.addEventListener('DOMContentLoaded', function() {
    if (isAuthenticated()) {
        const currentPage = window.location.pathname;
        if (currentPage.includes('login.html') || currentPage.includes('register.html')) {
            window.location.href = '/frontend/pages/dashboard.html';
        }
    }
});
