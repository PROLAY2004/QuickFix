// settings.js
document.addEventListener('DOMContentLoaded', function() {
    // Toggle switches functionality
    document.querySelectorAll('.toggle-switch input').forEach(switchInput => {
        switchInput.addEventListener('change', function() {
            const parentCard = this.closest('.settings-card');
            if (parentCard) {
                parentCard.classList.add('updated');
                setTimeout(() => {
                    parentCard.classList.remove('updated');
                }, 1000);
            }
        });
    });
    
    // Delete account modal
    const deleteModal = document.getElementById('deleteModal');
    const deleteBtn = document.getElementById('deleteAccountBtn');
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.cancel-btn');
    const confirmDelete = document.querySelector('.confirm-delete-btn');
    const confirmCheckbox = document.getElementById('confirmDelete');
    
    deleteBtn.addEventListener('click', function() {
        deleteModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    });
    
    closeModal.addEventListener('click', function() {
        deleteModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    });
    
    cancelBtn.addEventListener('click', function() {
        deleteModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    });
    
    confirmCheckbox.addEventListener('change', function() {
        confirmDelete.disabled = !this.checked;
    });
    
    confirmDelete.addEventListener('click', function() {
        if (!confirmDelete.disabled) {
            // In a real app, you would send a request to delete the account
            alert('Account deletion request received. Your account will be processed for deletion.');
            deleteModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === deleteModal) {
            deleteModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
    
    // Language select change
    const languageSelect = document.querySelector('.language-select');
    if (languageSelect) {
        languageSelect.addEventListener('change', function() {
            alert('Language preference updated to: ' + this.options[this.selectedIndex].text);
        });
    }
    
    // Check for updates
    const updateBtn = document.querySelector('.update-btn');
    if (updateBtn) {
        updateBtn.addEventListener('click', function() {
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Checking...';
            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-check-circle"></i> Up to date';
                setTimeout(() => {
                    this.innerHTML = 'Check for Updates';
                }, 2000);
            }, 1500);
        });
    }
    
    // Logout all devices
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to log out of all devices?')) {
                // In a real app, you would send a request to invalidate all sessions
                alert('You have been logged out of all devices.');
            }
        });
    }
    
    // Download data
    const downloadBtn = document.querySelector('.download-btn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Preparing data...';
            setTimeout(() => {
                // In a real app, this would trigger a download
                alert('Your data download has started. Check your downloads folder.');
                this.innerHTML = '<i class="fas fa-download"></i> Download Your Data';
            }, 2000);
        });
    }
});