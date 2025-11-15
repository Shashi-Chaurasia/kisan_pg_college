document.addEventListener("DOMContentLoaded", () => {
    const committeeLinks = document.querySelectorAll('.committee-link');
    const committeeMembersContainer = document.getElementById('committee-members');
    const committeeTitle = document.getElementById('committee-title');
    const modal = document.getElementById('member-modal');
    const closeModal = modal.querySelector('.close-modal');

    const loadCommitteeMembers = (committeeId) => {
        // Show loading state
        committeeMembersContainer.innerHTML = '<div class="loading-spinner">Loading members...</div>';
        committeeTitle.textContent = 'Loading...';
        
        fetch(`/api/committees/${committeeId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to load committee data');
                }
                return response.json();
            })
            .then(data => {
                committeeTitle.textContent = data.name;
                
                if (data.members && data.members.length > 0) {
                    committeeMembersContainer.innerHTML = data.members.map(member => `
                        <div class="member">
                            <h4>${escapeHtml(member.name)}</h4>
                            <p>${escapeHtml(member.designation)}</p>
                            <button class="view-member-btn" data-member='${JSON.stringify(member)}'>View Details</button>
                        </div>
                    `).join('');
                } else {
                    committeeMembersContainer.innerHTML = '<p class="no-members">No members found for this committee.</p>';
                }
            })
            .catch(error => {
                console.error('Error loading members:', error);
                committeeMembersContainer.innerHTML = '<p class="error-message">Failed to load members. Please try again.</p>';
                committeeTitle.textContent = 'Error';
            });
    };
    
    // Helper function to escape HTML and prevent XSS
    const escapeHtml = (text) => {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text ? text.replace(/[&<>"']/g, m => map[m]) : '';
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
            const committeeId = link.getAttribute('data-committee-id');
            if (committeeId) {
                loadCommitteeMembers(committeeId);
            }
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