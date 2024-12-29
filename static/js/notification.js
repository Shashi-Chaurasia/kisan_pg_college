document.addEventListener("DOMContentLoaded", function () {
    const notificationList = document.getElementById("notification-list");
    const newIndicator = document.getElementById("new-notification-indicator");

    // Scroll notifications
    setInterval(() => {
        if (notificationList.children.length > 1) {
            const firstChild = notificationList.firstElementChild;
            notificationList.appendChild(firstChild);
        }
    }, 3000);

    // Example of adding a new notification dynamically
    function addNewNotification(message, id) {
        const newNotification = document.createElement("li");
        newNotification.innerHTML = `<a href="/notification/${id}">${message}</a>`;
        notificationList.appendChild(newNotification);

        // Show new notification indicator
        newIndicator.style.display = "inline";
        setTimeout(() => {
            newIndicator.style.display = "none";
        }, 5000);
    }

    // Test: Add a new notification after 5 seconds
    setTimeout(() => {
        addNewNotification("Urgent: System maintenance scheduled tonight!", 999);
    }, 5000);
});