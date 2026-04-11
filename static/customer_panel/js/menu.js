// Save the scroll position before the page unloads
window.addEventListener('beforeunload', () => {
    sessionStorage.setItem('scrollPosition', window.scrollY);
});

// Restore the scroll position when the page loads
window.addEventListener('load', () => {
    const scrollPos = sessionStorage.getItem('scrollPosition');
    if (scrollPos) {
        window.scrollTo(0, parseInt(scrollPos));
        sessionStorage.removeItem('scrollPosition'); // Clear it after use
    }
});
