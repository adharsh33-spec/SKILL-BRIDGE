/* Dashboard JavaScript */

let currentUserId = null;
let userSkills = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    requireAuth();
    initializeDashboard();
    setupEventListeners();
});

// Initialize dashboard with user data
async function initializeDashboard() {
    const user = getStoredUser();
    if (user) {
        currentUserId = user.id;
        document.getElementById('userName').textContent = user.full_name;
        document.getElementById('userEmail').textContent = user.email;
        
        // Load user data
        await loadUserSkills();
        await loadRecommendations();
        await loadCertificates();
    }
}

// Setup event listeners for navigation
function setupEventListeners() {
    const sidebarLinks = document.querySelectorAll('.sidebar-menu a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all sections
            document.querySelectorAll('.content-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Remove active class from all links
            sidebarLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Get the target section
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });
    
    // Set first link as active
    if (sidebarLinks.length > 0) {
        sidebarLinks[0].classList.add('active');
        document.getElementById('dashboard').classList.add('active');
    }
}

// Load user skills
async function loadUserSkills() {
    const response = await apiCall(`/api/skills/user/${currentUserId}`);
    
    if (response.status === 'success') {
        userSkills = response.data || [];
        displayUserSkills();
        document.getElementById('skillCount').textContent = userSkills.length;
    }
}

// Display user skills
function displayUserSkills() {
    const skillsList = document.getElementById('skillsList');
    skillsList.innerHTML = '';
    
    if (userSkills.length === 0) {
        skillsList.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-light);">No skills added yet. Click "Add Skill" to get started!</p>';
        return;
    }
    
    userSkills.forEach(skill => {
        const skillElement = document.createElement('div');
        skillElement.className = 'skill-item';
        skillElement.innerHTML = `
            <h4>${skill.skill_name}</h4>
            <p>${skill.years_experience} years experience</p>
            <span class="skill-level">${skill.level}</span>
            <button class="btn btn-primary" style="margin-top: 1rem; width: 100%;" onclick="deleteSkill(${skill.id})">Delete</button>
        `;
        skillsList.appendChild(skillElement);
    });
}

// Add skill modal
function openAddSkillModal() {
    document.getElementById('addSkillModal').style.display = 'block';
}

function closeAddSkillModal() {
    document.getElementById('addSkillModal').style.display = 'none';
}

// Handle add skill form
document.addEventListener('DOMContentLoaded', function() {
    const addSkillForm = document.getElementById('addSkillForm');
    if (addSkillForm) {
        addSkillForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const skillData = {
                user_id: currentUserId,
                skill_name: document.getElementById('skillName').value,
                level: document.getElementById('skillLevel').value,
                years_experience: parseInt(document.getElementById('yearsExp').value)
            };
            
            const response = await apiCall('/api/skills/add', 'POST', skillData);
            
            if (response.status === 'success') {
                closeAddSkillModal();
                addSkillForm.reset();
                await loadUserSkills();
                showNotification('Skill added successfully!', 'success');
            } else {
                showNotification('Failed to add skill', 'error');
            }
        });
    }
});

// Delete skill
async function deleteSkill(skillId) {
    if (confirm('Are you sure you want to delete this skill?')) {
        const response = await apiCall(`/api/skills/${skillId}`, 'DELETE');
        
        if (response.status === 'success') {
            await loadUserSkills();
            showNotification('Skill deleted successfully!', 'success');
        } else {
            showNotification('Failed to delete skill', 'error');
        }
    }
}

// Load recommendations
async function loadRecommendations() {
    const response = await apiCall(`/api/recommendations/user/${currentUserId}`);
    
    if (response.status === 'success') {
        displayRecommendations(response.data || []);
        document.getElementById('jobCount').textContent = (response.data || []).length;
    }
}

// Display recommendations
function displayRecommendations(recommendations) {
    const recList = document.getElementById('recommendationsList');
    recList.innerHTML = '';
    
    if (recommendations.length === 0) {
        recList.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-light);">No recommendations yet. Generate recommendations based on your skills!</p>';
        return;
    }
    
    recommendations.forEach(job => {
        const recElement = document.createElement('div');
        recElement.className = 'recommendation-item';
        recElement.innerHTML = `
            <h4>${job.title}</h4>
            <p><strong>Company:</strong> ${job.company || 'N/A'}</p>
            <p><strong>Category:</strong> ${job.category || 'N/A'}</p>
            <p><strong>Salary:</strong> ${job.salary_range || 'N/A'}</p>
            <span class="match-score">${job.match_score || 0}% Match</span>
        `;
        recList.appendChild(recElement);
    });
}

// Generate recommendations
async function generateRecommendations() {
    if (userSkills.length === 0) {
        showNotification('Please add at least one skill first!', 'error');
        return;
    }
    
    const response = await apiCall(`/api/recommendations/generate/${currentUserId}`);
    
    if (response.status === 'success') {
        await loadRecommendations();
        showNotification('Recommendations generated successfully!', 'success');
    } else {
        showNotification('Failed to generate recommendations', 'error');
    }
}

// Load certificates
async function loadCertificates() {
    // This would call an API endpoint for certificates
    // For now, we'll display a placeholder
    const certList = document.getElementById('certificatesList');
    certList.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-light);">No certificates earned yet. Start upskilling to earn blockchain-based certificates!</p>';
    document.getElementById('certCount').textContent = '0';
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `message ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    const modal = document.getElementById('addSkillModal');
    if (modal && e.target === modal) {
        closeAddSkillModal();
    }
});
