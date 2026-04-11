function initInfiniteScroll(trackId) {
    const track = document.getElementById(trackId);
    const cards = Array.from(track.children);

    // 1. Clone items to fill space and ensure no gaps
    cards.forEach(card => {
        const clone = card.cloneNode(true);
        track.appendChild(clone);
    });

    let scrollAmount = 0;
    const speed = 0.5; // Adjust speed (higher is faster)

    function step() {
        scrollAmount -= speed;

        // 2. Reset scroll once half the track (the original items) has passed
        // This creates the "Infinite" illusion
        if (Math.abs(scrollAmount) >= track.scrollWidth / 2) {
            scrollAmount = 0;
        }

        track.style.transform = `translateX(${scrollAmount}px)`;
        requestAnimationFrame(step);
    }

    // Start animation
    requestAnimationFrame(step);

    // Optional: Pause on hover
    track.addEventListener('mouseenter', () => { /* Logic to stop animation if desired */ });
}

document.addEventListener("DOMContentLoaded", () => {
    initInfiniteScroll('dish-track');
    initInfiniteScroll('review-track');
});
