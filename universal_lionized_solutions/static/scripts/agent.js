// Initialize Feather Icons
document.addEventListener('DOMContentLoaded', () => {
    feather.replace();
    showContent('properties'); // Show default content
});

// Sidebar Toggle
let sidebarOpen = true;

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const overlay = document.getElementById('overlay');
    
    sidebarOpen = !sidebarOpen;
    
    if (sidebarOpen) {
        sidebar.classList.remove('-translate-x-full');
        mainContent.classList.remove('ml-0');
        mainContent.classList.add('ml-64');
        if (window.innerWidth < 1024) {
            overlay.classList.remove('hidden');
        }
    } else {
        sidebar.classList.add('-translate-x-full');
        mainContent.classList.remove('ml-64');
        mainContent.classList.add('ml-0');
        overlay.classList.add('hidden');
    }
}

// Initialize sidebar based on screen size
function initializeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    
    if (window.innerWidth >= 1024) {
        sidebar.classList.remove('-translate-x-full');
        mainContent.classList.add('ml-64');
        sidebarOpen = true;
    } else {
        sidebar.classList.add('-translate-x-full');
        mainContent.classList.remove('ml-64');
        sidebarOpen = false;
    }
}

// User Dropdown Toggle
function toggleDropdown() {
    const dropdown = document.getElementById('userDropdown');
    dropdown.classList.toggle('hidden');
}

// Content Switching
function showContent(sectionId) {
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.add('hidden');
    });
    
    document.getElementById(sectionId).classList.remove('hidden');
    
    document.querySelectorAll('[data-nav-button]').forEach(button => {
        button.classList.remove('bg-amber-50', 'text-amber-600');
    });
    
    const activeButton = document.querySelector(`[onclick="showContent('${sectionId}')"]`);
    activeButton.classList.add('bg-amber-600', 'text-gray-600');
}

// Copy Referral Link
function copyReferralLink() {
    const linkInput = document.getElementById('referral-link-input');
    linkInput.select();
    document.execCommand('copy');
    alert('Referral link copied to clipboard!');
}