var navLinks= document.getElementById("navLinks");

function showmenu(){
    navLinks.style.right="0";
}
function hidemenu(){
    navLinks.style.right="-200px";
}

document.addEventListener("DOMContentLoaded", function () {
    const readMoreBtn = document.getElementById("read-more-btn");
    const aboutText = document.getElementById("about-text");

    readMoreBtn.addEventListener("click", function () {
        if (aboutText.classList.contains("truncate")) {
            aboutText.classList.remove("truncate");
            aboutText.classList.add("expand");
            readMoreBtn.textContent = "Read Less";
        } else {
            aboutText.classList.remove("expand");
            aboutText.classList.add("truncate");
            readMoreBtn.textContent = "Read More";
        }
    });
});

// document.addEventListener('contextmenu', event => event.preventDefault());