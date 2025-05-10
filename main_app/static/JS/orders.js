document.addEventListener('DOMContentLoaded', function() {
    // Filter functionality
    const statusFilter = document.getElementById('status-filter');
    const orderCards = document.querySelectorAll('.order-card');
    
    statusFilter.addEventListener('change', function() {
        const selectedStatus = this.value;
        
        orderCards.forEach(card => {
            if (selectedStatus === 'all' || card.dataset.status === selectedStatus) {
                card.style.display = 'block';
                card.classList.add('animate__animated', 'animate__fadeIn');
            } else {
                card.style.display = 'none';
            }
        });
    });
    
    // Time filter functionality would be similar
    
    // Search functionality
    const searchInput = document.querySelector('.search-input');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        orderCards.forEach(card => {
            const orderId = card.querySelector('.order-id').textContent.toLowerCase();
            const orderDate = card.querySelector('.order-date').textContent.toLowerCase();
            const productNames = Array.from(card.querySelectorAll('.product-details h4'))
                .map(el => el.textContent.toLowerCase());
            
            if (orderId.includes(searchTerm) || 
                orderDate.includes(searchTerm) || 
                productNames.some(name => name.includes(searchTerm))) {
                card.style.display = 'block';
                card.classList.add('animate__animated', 'animate__fadeIn');
            } else {
                card.style.display = 'none';
            }
        });
    });
    
    // Add hover effects to product images
    const productImages = document.querySelectorAll('.product-image');
    
    productImages.forEach(image => {
        image.addEventListener('mouseenter', function() {
            this.querySelector('img').style.transform = 'scale(1.05)';
        });
        
        image.addEventListener('mouseleave', function() {
            this.querySelector('img').style.transform = 'scale(1)';
        });
    });
    
    // Remove animation classes after they complete
    const animatedElements = document.querySelectorAll('.animate__animated');
    
    animatedElements.forEach(el => {
        el.addEventListener('animationend', function() {
            this.classList.remove('animate__animated', 'animate__fadeIn');
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // Filter functionality
    const statusFilter = document.getElementById('status-filter');
    const orderCards = document.querySelectorAll('.order-card');
    
    statusFilter.addEventListener('change', function() {
        const selectedStatus = this.value;
        
        orderCards.forEach(card => {
            if (selectedStatus === 'all' || card.dataset.status === selectedStatus) {
                card.style.display = 'block';
                card.classList.add('animate__animated', 'animate__fadeIn');
            } else {
                card.style.display = 'none';
            }
        });
    });
    
    // Time filter functionality would be similar
    
    // Search functionality
    const searchInput = document.querySelector('.search-input');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        orderCards.forEach(card => {
            const orderId = card.querySelector('.order-id').textContent.toLowerCase();
            const orderDate = card.querySelector('.order-date').textContent.toLowerCase();
            const productNames = Array.from(card.querySelectorAll('.product-details h4'))
                .map(el => el.textContent.toLowerCase());
            
            if (orderId.includes(searchTerm) || 
                orderDate.includes(searchTerm) || 
                productNames.some(name => name.includes(searchTerm))) {
                card.style.display = 'block';
                card.classList.add('animate__animated', 'animate__fadeIn');
            } else {
                card.style.display = 'none';
            }
        });
    });
    
    // Add hover effects to product images
    const productImages = document.querySelectorAll('.product-image');
    
    productImages.forEach(image => {
        image.addEventListener('mouseenter', function() {
            this.querySelector('img').style.transform = 'scale(1.05)';
        });
        
        image.addEventListener('mouseleave', function() {
            this.querySelector('img').style.transform = 'scale(1)';
        });
    });
    
    // Remove animation classes after they complete
    const animatedElements = document.querySelectorAll('.animate__animated');
    
    animatedElements.forEach(el => {
        el.addEventListener('animationend', function() {
            this.classList.remove('animate__animated', 'animate__fadeIn');
        });
    });
    
    // Add confirmation for cancel order
    const cancelButtons = document.querySelectorAll('.cancel-order');
    
    cancelButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Are you sure you want to cancel this order?')) {
                // In a real app, you would make an API call here
                const orderCard = this.closest('.order-card');
                orderCard.querySelector('.order-status').className = 'order-status cancelled';
                orderCard.querySelector('.order-status span').textContent = 'Cancelled';
                orderCard.querySelector('.order-status i').className = 'fas fa-times-circle';
                orderCard.dataset.status = 'cancelled';
                
                // Update the order date to show cancellation
                const dateElement = orderCard.querySelector('.order-date');
                dateElement.textContent = `Cancelled on ${new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}`;
                
                // Update the delivery info
                const deliveryInfo = orderCard.querySelector('.delivery-info h5');
                deliveryInfo.textContent = new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
                
                // Remove the cancel button
                this.remove();
                
                // Add reorder button
                const actionsDiv = orderCard.querySelector('.order-actions');
                const reorderBtn = document.createElement('button');
                reorderBtn.className = 'action-btn reorder';
                reorderBtn.innerHTML = '<i class="fas fa-redo"></i> Reorder';
                actionsDiv.appendChild(reorderBtn);
                
                // Show success message
                alert('Your order has been cancelled successfully.');
            }
        });
    });
});