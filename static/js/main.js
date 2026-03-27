/**
 * Main JavaScript File
 * Common functionality and utilities
 */

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (mobileMenuToggle && navLinks && !mobileMenuToggle.contains(e.target) && !navLinks.contains(e.target)) {
            navLinks.classList.remove('active');
        }
    });

    // Add scroll effect to navbar
    const navbar = document.querySelector('.landing-nav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });

    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#ef4444';
                    setTimeout(() => {
                        field.style.borderColor = '';
                    }, 3000);
                }
            });

            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields', 'error');
            }
        });
    });

    // Add animation to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.dashboard-card, .about-section, .feature-item, .course-card, .info-card').forEach(card => {
        observer.observe(card);
    });
});

// Utility function to show notifications
function showNotification(message, type = 'success') {
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    
    const flashMessage = document.createElement('div');
    flashMessage.className = `flash-message flash-${type}`;
    flashMessage.innerHTML = `
        <span>${message}</span>
        <button class="close-flash" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    flashContainer.appendChild(flashMessage);
    
    setTimeout(() => {
        flashMessage.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => flashMessage.remove(), 300);
    }, 5000);
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

// Mobile sidebar toggle function
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay') || createSidebarOverlay();
    
    if (sidebar) {
        sidebar.classList.toggle('show');
        overlay.classList.toggle('show');
    }
}

function createSidebarOverlay() {
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    overlay.onclick = toggleSidebar;
    document.body.appendChild(overlay);
    return overlay;
}

// Close sidebar when clicking on nav items (mobile)
document.addEventListener('DOMContentLoaded', function() {
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                toggleSidebar();
            }
        });
    });
});

// Add slide out animation for flash messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);
