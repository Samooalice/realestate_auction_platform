/**
 * Main JavaScript - Real Estate Auction Platform
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS Animation
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 50
        });
    }

    // Navbar Scroll Effect
    initNavbarScroll();

    // Back to Top Button
    initBackToTop();

    // Toast Auto Dismiss
    initToastAutoDismiss();

    // Smooth Scroll
    initSmoothScroll();

    // Form Validation
    initFormValidation();

    // Number Counter Animation
    initNumberCounter();
});

/**
 * Navbar Scroll Effect
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

/**
 * Back to Top Button
 */
function initBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');
    if (!backToTopBtn) return;

    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });

    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * Toast Auto Dismiss
 */
function initToastAutoDismiss() {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(function(toast) {
        setTimeout(function() {
            const bsToast = bootstrap.Toast.getOrCreateInstance(toast);
            bsToast.hide();
        }, 5000);
    });
}

/**
 * Smooth Scroll for Anchor Links
 */
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Form Validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

/**
 * Number Counter Animation
 */
function initNumberCounter() {
    const counters = document.querySelectorAll('.stat-number, .hero-stat-number');

    const options = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, options);

    counters.forEach(function(counter) {
        observer.observe(counter);
    });
}

function animateCounter(element) {
    const text = element.textContent;
    const match = text.match(/[\d,]+/);
    if (!match) return;

    const target = parseInt(match[0].replace(/,/g, ''));
    const duration = 2000;
    const start = performance.now();
    const prefix = text.split(match[0])[0];
    const suffix = text.split(match[0])[1] || '';

    function update(currentTime) {
        const elapsed = currentTime - start;
        const progress = Math.min(elapsed / duration, 1);
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(target * easeProgress);

        element.textContent = prefix + current.toLocaleString() + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

/**
 * Bookmark Toggle (AJAX)
 */
function toggleBookmark(propertyId) {
    fetch(`/properties/bookmark/${propertyId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        const btn = document.querySelector(`[data-bookmark="${propertyId}"]`);
        if (btn) {
            const icon = btn.querySelector('i');
            if (data.is_bookmarked) {
                icon.classList.remove('bi-heart');
                icon.classList.add('bi-heart-fill');
                btn.classList.add('text-danger');
            } else {
                icon.classList.remove('bi-heart-fill');
                icon.classList.add('bi-heart');
                btn.classList.remove('text-danger');
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

/**
 * Get CSRF Token from Cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Format Currency (Korean Won)
 */
function formatCurrency(amount) {
    if (amount >= 100000000) {
        return (amount / 100000000).toFixed(1) + '억';
    } else if (amount >= 10000) {
        return (amount / 10000).toFixed(0) + '만';
    }
    return amount.toLocaleString();
}

/**
 * Debounce Function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
