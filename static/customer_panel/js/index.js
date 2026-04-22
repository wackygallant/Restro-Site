function initCarousel(trackId, prevBtnId, nextBtnId) {
    const track = document.getElementById(trackId);
    const prevBtn = document.getElementById(prevBtnId);
    const nextBtn = document.getElementById(nextBtnId);

    let cards = Array.from(track.children);

    // ❗ Disable buttons if not enough items
    if (cards.length <= 3) {
        if (prevBtn) prevBtn.style.display = "none";
        if (nextBtn) nextBtn.style.display = "none";
        return;
    }

    let index = 1;

    // Clone for infinite loop
    const firstClone = cards[0].cloneNode(true);
    const lastClone = cards[cards.length - 1].cloneNode(true);

    track.appendChild(firstClone);
    track.insertBefore(lastClone, cards[0]);

    cards = Array.from(track.children);

    function updateCarousel() {
        const width = cards[0].offsetWidth;
        track.style.transform = `translateX(-${index * width}px)`;

        cards.forEach(card => card.classList.remove("active"));
        if (cards[index]) cards[index].classList.add("active");
    }

    nextBtn.onclick = () => {
        index++;
        track.style.transition = "transform 0.6s ease";
        updateCarousel();
    };

    prevBtn.onclick = () => {
        index--;
        track.style.transition = "transform 0.6s ease";
        updateCarousel();
    };

    track.addEventListener("transitionend", () => {
        if (index === cards.length - 1) {
            track.style.transition = "none";
            index = 1;
            updateCarousel();
        }

        if (index === 0) {
            track.style.transition = "none";
            index = cards.length - 2;
            updateCarousel();
        }
    });

    updateCarousel();
}

document.addEventListener("DOMContentLoaded", () => {
    initCarousel("dish-track", "dish-prev", "dish-next");
    initCarousel("review-track", "review-prev", "review-next");
});