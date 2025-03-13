document.addEventListener('DOMContentLoaded', function() {
    // Find popup elements
    const popupBanner = document.getElementById('popupBanner');

    // Handle the popup banner if it exists (only on homepage)
    if (popupBanner) {
        const popupCloseBtn = document.getElementById('popupCloseBtn');
        const popupCloseBtn2 = document.getElementById('popupCloseBtn2');

        // Show the popup immediately on page load and when redirecting to homepage
        popupBanner.style.display = 'flex';

        // Add a slight delay to allow the CSS animation to work
        setTimeout(() => {
            popupBanner.classList.add('show');
        }, 100);

        // Helper function to close popup with animation
        function closePopup() {
            popupBanner.classList.remove('show');
            setTimeout(() => {
                popupBanner.style.display = 'none';
            }, 300);
        }

        // Close popup when clicking the close button
        if (popupCloseBtn) {
            popupCloseBtn.addEventListener('click', function() {
                closePopup();
            });
        }

        // Additional close button
        if (popupCloseBtn2) {
            popupCloseBtn2.addEventListener('click', function() {
                closePopup();
            });
        }

        // Close on backdrop click
        popupBanner.addEventListener('click', function(e) {
            if (e.target === popupBanner) {
                closePopup();
            }
        });
    }
});