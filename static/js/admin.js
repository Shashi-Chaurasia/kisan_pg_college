function openModal(type, id = null) {
    const modal = document.getElementById(`${type}-modal`);
    const title = document.getElementById(`${type}-modal-title`);
    const form = document.getElementById(`${type}-modal-form`);

    // Reset form for new entity (Add)
    form.reset();
    document.getElementById(`${type}-id`).value = id || "";

    if (id) {
        // Call the separate edit function
        editEntity(type, id);
    } else {
        title.textContent = `Add ${capitalize(type)}`;
        modal.style.display = "block";
    }
}

// Separate Edit Function
function editEntity(type, id) {
    const modal = document.getElementById(`${type}-modal`);
    const title = document.getElementById(`${type}-modal-title`);
    const form = document.getElementById(`${type}-modal-form`);

    title.textContent = `Edit ${capitalize(type)}`;

    // Fetch the existing data
    fetch(`/admin/manage/${type}/edit/${id}`)
        .then(response => response.json())
        .then(entity => {
            if (entity) {
                for (const key in entity) {
                    const formElement = form.elements[key];
                    if (formElement) {
                        formElement.value = entity[key] || ''; // Set the value or empty if not present
                    }
                }
                modal.style.display = "block"; // Show the modal after data is loaded
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert('An error occurred while fetching data.');
        });
}

// Form Submit Function
function handleFormSubmit(type) {
    const form = document.getElementById(`${type}-modal-form`);
    form.onsubmit = function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const id = document.getElementById(`${type}-id`).value;
        const url = id
            ? `/admin/manage/${type}/edit/${id}` // Edit API
            : `/admin/manage/${type}/add`; // Add API

        fetch(url, {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                alert("Operation successful!");
                location.reload(); // Reload the page to reflect changes
            } else {
                return response.json().then(data => {
                    alert(`Error: ${data.message || "Operation failed"}`);
                });
            }
        })
        .catch(error => {
            console.error("Error during form submission:", error);
            alert("An error occurred while saving the data.");
        });
    };
}
// Modal Close Function
function closeModal(type) {
    const modal = document.getElementById(`${type}-modal`);
    modal.style.display = "none";
}

// Capitalize function for dynamic titles
function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


// Delete Entity (Faculty, News, Course)
function deleteEntity(type, id) {
    if (confirm(`Are you sure you want to delete this ${type}?`)) {
        // Define base path for different entity types
        let basePath = "";

        switch (type) {
            case "faculty":
                basePath = "/admin/manage/faculty/delete/";
                break;
            case "news":
                basePath = "/admin/manage/news/delete/";
                break;
            case "course":
                basePath = "/admin/manage/course/delete/";
                break;
            default:
                alert("Invalid type!");
                return;
        }

        window.location.href = `${basePath}${id}`;
    }
}

// Global Modal Close on Click Outside
window.onclick = function (event) {
    const modals = document.getElementsByClassName("modal");
    for (let i = 0; i < modals.length; i++) {
        if (event.target == modals[i]) {
            modals[i].style.display = "none";
        }
    }
};

// Add Event Listeners for Add Buttons (Faculty, News, Courses)
document.addEventListener("DOMContentLoaded", function () {
    // Adding event listeners to Add Faculty, News, and Course buttons
    const addButtons = document.querySelectorAll('.btn-add');
    addButtons.forEach(button => {
        button.addEventListener('click', function () {
            const type = button.getAttribute('data-type');
            openModal(type);  // Open respective modal
        });
    });
    
    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);