document.addEventListener("DOMContentLoaded", function() {
    function initTeamCarousel() {
        const track = document.getElementById('team-track');
        const container = document.getElementById('team-carousel');
        
        // Safety check to prevent errors if elements aren't found
        if (!track || !container) return;
        
        const cards = Array.from(track.children);
        if (cards.length === 0) return;

        // 1. Clone cards to fill the track for a seamless loop
        cards.forEach(card => {
            const clone = card.cloneNode(true);
            track.appendChild(clone);
        });
        
        let currentPosition = 0;
        const autoScrollSpeed = 0.5; // Very smooth slow crawl
        let isPaused = false;
        
        function animate() {
            if (!isPaused) {
                currentPosition -= autoScrollSpeed;
                
                // 2. Reset logic: track.scrollWidth / 2 represents the original set of cards
                if (Math.abs(currentPosition) >= track.scrollWidth / 2) {
                    currentPosition = 0;
                }
                
                track.style.transform = `translateX(${currentPosition}px)`;
            }
            requestAnimationFrame(animate);
        }
        
        // Pause when mouse is over the team section
        container.addEventListener('mouseenter', () => isPaused = true);
        container.addEventListener('mouseleave', () => isPaused = false);
        
        animate();
    }
    
    initTeamCarousel();
});