document.addEventListener("DOMContentLoaded", () => {
    const committeeLinks = document.querySelectorAll('.committee-link');
    const committeeMembersContainer = document.getElementById('committee-members');
    const committeeTitle = document.getElementById('committee-title');
    const modal = document.getElementById('member-modal');
    const closeModal = modal.querySelector('.close-modal');

    const loadCommitteeMembers = (committeeId) => {
        fetch(`/api/committees/${committeeId}`)
            .then(response => response.json())
            .then(data => {
                committeeTitle.textContent = data.name;
                committeeMembersContainer.innerHTML = data.members.map(member => `
                    <div class="member">
                        <h4>${member.name}</h4>
                        <p>${member.designation}</p>
                        <button class="view-member-btn" data-member='${JSON.stringify(member)}'>View Details</button>
                    </div>
                `).join('');
            })
            .catch(error => console.error('Error loading members:', error));
    };

    const openModal = (member) => {
        document.getElementById('member-photo').src = member.photo || '';
        document.getElementById('member-name').textContent = member.name;
        document.getElementById('member-designation').textContent = member.designation;
        document.getElementById('member-bio').textContent = member.bio;
        modal.style.display = 'block';
    };

    committeeLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const committeeId = e.target.getAttribute('data-committee-id');
            loadCommitteeMembers(committeeId);
        });
    });

    committeeMembersContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('view-member-btn')) {
            const member = JSON.parse(e.target.getAttribute('data-member'));
            openModal(member);
        }
    });

    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});