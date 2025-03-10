// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Flash message auto-dismiss with animation
    var flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(flash) {
        flash.style.animation = 'slideIn 0.3s ease-out forwards';
        setTimeout(function() {
            flash.style.animation = 'fadeOut 0.3s ease-in forwards';
            setTimeout(function() {
                var alert = new bootstrap.Alert(flash);
                alert.close();
            }, 300);
        }, 5000);
    });

    // Form validation with animated feedback
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                // Add shake animation to invalid fields
                form.querySelectorAll(':invalid').forEach(function(field) {
                    field.style.animation = 'shake 0.3s ease-in-out';
                    field.addEventListener('animationend', function() {
                        field.style.animation = '';
                    });
                });
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Carousel auto-play with smooth transitions
    var carousels = document.querySelectorAll('.carousel');
    carousels.forEach(function(carousel) {
        new bootstrap.Carousel(carousel, {
            interval: 5000,
            wrap: true
        });
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
                element.classList.add('animate');
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
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
            link.style.animation = 'fadeIn 0.3s ease-out';
        }
    });

    // Add animation classes to cards
    document.querySelectorAll('.card').forEach(function(card, index) {
        card.classList.add('animate-on-scroll');
        card.style.animationDelay = (index * 0.1) + 's';
    });
});

// Add necessary keyframe animations
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    @keyframes slideIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    .animate-on-scroll {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.6s ease, transform 0.6s ease;
    }
    .animate-on-scroll.animate {
        opacity: 1;
        transform: translateY(0);
    }
`;
document.head.appendChild(style);