// Back to top button functionality
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    var backToTopButton = document.getElementById("backToTop");
    if (backToTopButton) {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            backToTopButton.style.display = "block";
        } else {
            backToTopButton.style.display = "none";
        }
    }
}

function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

// Initialize any tooltips
document.addEventListener("DOMContentLoaded", function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Registration form tabs functionality
    var registrationTabs = document.getElementById('registrationTabs');
    if (registrationTabs) {
        var tabs = new bootstrap.Tab(document.querySelector('#registrationTabs .nav-link.active'));
        
        // Store the active tab in session storage
        document.querySelectorAll('#registrationTabs .nav-link').forEach(tab => {
            tab.addEventListener('shown.bs.tab', function (e) {
                sessionStorage.setItem('activeRegistrationTab', e.target.id);
            });
        });
        
        // Restore active tab from session storage
        var activeTab = sessionStorage.getItem('activeRegistrationTab');
        if (activeTab) {
            const tabToActivate = document.getElementById(activeTab);
            if (tabToActivate) {
                new bootstrap.Tab(tabToActivate).show();
            }
        }
    }

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Responsive table wrapper
    var tables = document.querySelectorAll('table');
    tables.forEach(function(table) {
        if (!table.parentElement.classList.contains('table-responsive')) {
            var wrapper = document.createElement('div');
            wrapper.classList.add('table-responsive');
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });

    // Active navigation highlighting with animation
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentLocation || 
            (currentLocation.includes('/dashboard') && href.includes('/dashboard'))) {
            link.classList.add('active');
            link.style.animation = 'fadeIn 0.3s ease-out';
        }
    });

    // Add animation classes to elements
    const animateElements = document.querySelectorAll('.card, .section-title, .btn-lg, .hero-content');
    animateElements.forEach(function(element, index) {
        element.classList.add('animate-on-scroll');
        element.style.animationDelay = (index * 0.1) + 's';
        element.style.opacity = '0';
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                document.querySelector(targetId).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Animate elements on scroll
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        elements.forEach(function(element) {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('animate-fadeInUp');
                element.style.opacity = '1';
            }
        });
    };

    // Add scroll event listener for animations
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Initial check for visible elements

    // Dynamic year in footer
    var yearElement = document.querySelector('.current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

    // Mobile navigation enhancement
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    }

    // Add hover effect to cards in quick links and registration cards
    const hoverCards = document.querySelectorAll('.quick-links .card, .hover-card');
    hoverCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Animated counter for statistics on dashboard
    const counters = document.querySelectorAll('.counter-value');
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const duration = 1500;
        const increment = target / duration * 10;
        let current = 0;

        const updateCounter = () => {
            current += increment;
            counter.innerText = Math.floor(current);

            if (current < target) {
                setTimeout(updateCounter, 10);
            } else {
                counter.innerText = target;
            }
        };

        if (isElementInViewport(counter)) {
            updateCounter();
        } else {
            window.addEventListener('scroll', function scrollHandler() {
                if (isElementInViewport(counter)) {
                    updateCounter();
                    window.removeEventListener('scroll', scrollHandler);
                }
            });
        }
    });

    // Check if element is in viewport
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();

                // Add shake animation to invalid fields
                const invalidFields = form.querySelectorAll(':invalid');
                invalidFields.forEach(field => {
                    field.classList.add('shake-animation');
                    setTimeout(() => {
                        field.classList.remove('shake-animation');
                    }, 500);
                });
            }

            form.classList.add('was-validated');
        }, false);
    });

    // Image lazy loading
    const lazyImages = document.querySelectorAll('img[data-src]');
    lazyImages.forEach(img => {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    img.src = img.dataset.src;
                    observer.unobserve(img);
                }
            });
        });

        observer.observe(img);
    });

    // Dark/Light mode toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('dark-mode', isDarkMode);

            // Update toggle icon
            this.querySelector('i').classList.toggle('bi-moon-fill');
            this.querySelector('i').classList.toggle('bi-sun-fill');
        });

        // Check for saved theme preference
        const savedTheme = localStorage.getItem('dark-mode');
        if (savedTheme === 'true') {
            document.body.classList.add('dark-mode');
            themeToggle.querySelector('i').classList.remove('bi-moon-fill');
            themeToggle.querySelector('i').classList.add('bi-sun-fill');
        }
    }

    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const x = e.clientX - this.getBoundingClientRect().left;
            const y = e.clientY - this.getBoundingClientRect().top;

            const ripple = document.createElement('span');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            ripple.classList.add('ripple');

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Enhancement for mobile search
    const searchToggle = document.querySelector('.search-toggle');
    const searchForm = document.querySelector('.search-form');

    if (searchToggle && searchForm) {
        searchToggle.addEventListener('click', function() {
            searchForm.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Back to top button functionality
    var backToTopBtn = document.getElementById('backToTop');
    if (backToTopBtn) {
        // Show/hide the button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopBtn.style.display = 'block';
            } else {
                backToTopBtn.style.display = 'none';
            }
        });

        // Scroll to top when clicked
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }


    // Button ripple effect (already included above)

    // Add styles
    const style = document.createElement('style');
    style.innerHTML = `
        .btn {
            position: relative;
            overflow: hidden;
        }

        .ripple {
            position: absolute;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        }

        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }

        .shake-animation {
            animation: shake 0.5s linear;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }

        .search-form {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }

        .search-form.active {
            max-height: 50px;
        }

        .dark-mode {
            background-color: #222;
            color: #f8f9fa;
        }

        .dark-mode .card {
            background-color: #333;
            color: #f8f9fa;
        }

        .dark-mode .navbar-light {
            background-color: #333 !important;
        }

        .dark-mode .navbar-light .navbar-nav .nav-link {
            color: #f8f9fa;
        }

        #backToTop {
            display: none;
            position: fixed; /* Added for proper positioning */
            bottom: 20px; /* Adjust as needed */
            right: 20px; /* Adjust as needed */
            border-radius: 50%;
            width: 50px;
            height: 50px;
            text-align: center;
            line-height: 50px;
            padding: 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            cursor: pointer; /* Added for better usability */
            background-color: #4CAF50; /* Example color */
            color: white;
        }

        #backToTop i {
            font-size: 20px;
        }
    `;
    document.head.appendChild(style);
});
