// ──────────────────────────────────────────────
// Announcement Dismiss Script
// ──────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function () {
    const cross = document.getElementById('cross');
    const announcement = document.querySelector('.announcement');

    if (cross && announcement) {
        cross.addEventListener('click', function () {
            announcement.style.opacity = '0';
            announcement.style.maxHeight = '0';
            announcement.style.padding = '0 1.5rem';
            setTimeout(() => {
                announcement.style.display = 'none';
            }, 300);
        });
    }
});
