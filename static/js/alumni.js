let alumniIndex = 0;
let autoScrollInterval;

// Function to move the carousel
function moveAlumniSlide(direction) {
    const carousel = document.getElementById('alumni-carousel');
    const alumniCols = document.querySelectorAll('.alumni-col');
    const slideWidth = alumniCols[0].clientWidth + 20; // Includes 20px margin

    // Update the index
    alumniIndex += direction;
    if (alumniIndex < 0) {
        alumniIndex = alumniCols.length - 1;
    } else if (alumniIndex >= alumniCols.length) {
        alumniIndex = 0;
    }

    // Scroll the carousel
    carousel.style.transform = `translateX(-${alumniIndex * slideWidth}px)`;
}

// Function to start auto-scrolling
function startAutoScroll() {
    autoScrollInterval = setInterval(() => {
        moveAlumniSlide(1); // Automatically move to the next slide
    }, 3000); // Change slide every 3 seconds
}

// Function to stop auto-scrolling (useful for manual control)
function stopAutoScroll() {
    clearInterval(autoScrollInterval);
}

// Attach event listeners for manual control
document.querySelector('.prev-btn').addEventListener('click', () => {
    stopAutoScroll();
    moveAlumniSlide(-1);
    startAutoScroll(); // Restart auto-scroll
});

document.querySelector('.next-btn').addEventListener('click', () => {
    stopAutoScroll();
    moveAlumniSlide(1);
    startAutoScroll(); // Restart auto-scroll
});

// Initialize auto-scrolling on page load
window.onload = startAutoScroll;