let currentIndex = 0;
let slideInterval; // To hold the interval ID

function moveSlide(direction) {
    const carousel = document.getElementById("faculty-carousel");
    const faculties = document.querySelectorAll(".faculties-col");
    const visibleCount = 3; // Number of visible cards
    const totalCards = faculties.length;
    const totalSlides = Math.ceil(totalCards / visibleCount); // Total number of slides

    // Update currentIndex based on direction
    currentIndex += direction;

    // Handle wrapping
    if (currentIndex < 0) {
        currentIndex = totalSlides - 1; // Wrap to the last slide
    } else if (currentIndex >= totalSlides) {
        currentIndex = 0; // Wrap to the first slide
    }

    // Calculate the width per slide (if you are not already using a fixed width)
    const slideWidth = faculties[0].offsetWidth + 20; // 20px accounts for the gap between items
    const offset = -(currentIndex * slideWidth); // Slide width is dynamic based on content

    // Apply the offset to the carousel
    carousel.style.transform = `translateX(${offset}px)`;

    // Debugging logs
    console.log("Current Index:", currentIndex);
    console.log("Total Slides:", totalSlides);
    console.log("Total Cards:", totalCards);
}

function startAutoSlide() {
    slideInterval = setInterval(() => moveSlide(1), 3000); // Slide every 3 seconds
}

function stopAutoSlide() {
    clearInterval(slideInterval);
}

// Start the automatic slide when the page loads
document.addEventListener("DOMContentLoaded", startAutoSlide);

// Pause auto-slide on hover, resume on mouseout
document.getElementById("faculty-carousel").addEventListener("mouseover", stopAutoSlide);
document.getElementById("faculty-carousel").addEventListener("mouseout", startAutoSlide);