var navLinks = document.getElementById("navLinks");
var navOverlay = document.getElementById("navOverlay");

function showmenu() {
    if (navLinks) {
        navLinks.style.right = "0";
        // Show overlay
        if (navOverlay) {
            navOverlay.classList.add('active');
        }
        // Prevent body scroll when menu is open
        document.body.style.overflow = "hidden";
    }
}

function hidemenu() {
    if (navLinks) {
        navLinks.style.right = "-250px";
        // Hide overlay
        if (navOverlay) {
            navOverlay.classList.remove('active');
        }
        // Re-enable body scroll when menu is closed
        document.body.style.overflow = "auto";
    }
}

// Close menu when clicking on a link
if (navLinks) {
    var navLinksItems = navLinks.querySelectorAll('a');
    navLinksItems.forEach(function(link) {
        link.addEventListener('click', function() {
            hidemenu();
        });
    });
}

// Handle escape key to close menu
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        hidemenu();
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const readMoreBtn = document.getElementById("read-more-btn");
    const aboutText = document.getElementById("about-text");

    if (readMoreBtn && aboutText) {
        readMoreBtn.addEventListener("click", function () {
            if (aboutText.classList.contains("truncate")) {
                aboutText.classList.remove("truncate");
                aboutText.classList.add("expand");
                readMoreBtn.classList.add("expanded");
                readMoreBtn.querySelector('.btn-text').textContent = "कम पढ़ें";
            } else {
                aboutText.classList.remove("expand");
                aboutText.classList.add("truncate");
                readMoreBtn.classList.remove("expanded");
                readMoreBtn.querySelector('.btn-text').textContent = "और पढ़ें";
                // Scroll back to top of content
                aboutText.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    }
});

// document.addEventListener('contextmenu', event => event.preventDefault());