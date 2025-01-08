let currentIndex = 0;
let slideInterval; // To hold the interval ID

function moveSlide(direction) {
    const carousel = document.getElementById("faculty-carousel");
    const faculties = document.querySelectorAll(".faculties-col");
    const visibleCount = 3; // Number of visible cards per slide
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

    // Calculate the offset for the current slide
    const slideWidth = faculties[0].offsetWidth + 20; // Include gap between cards (adjust if needed)
    const offset = -(currentIndex * visibleCount * slideWidth); // Offset by the width of `visibleCount` cards

    // Apply the calculated offset to the carousel
    carousel.style.transform = `translateX(${offset}px)`;

    // Debugging logs
    console.log("Current Index:", currentIndex);
    console.log("Total Slides:", totalSlides);
    console.log("Total Cards:", totalCards);
    console.log("Visible Count:", visibleCount);
    console.log("Slide Width:", slideWidth);
    console.log("Offset:", offset);
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
const carousel = document.getElementById("faculty-carousel");
carousel.addEventListener("mouseover", stopAutoSlide);
carousel.addEventListener("mouseout", startAutoSlide);