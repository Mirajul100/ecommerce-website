// Cart state
let cart = [];
let selectedSizes = {};

// Initialize the store
document.addEventListener('DOMContentLoaded', function() {
    initializeCategoryFilters();
    initializeSizeSelection();
    initializeCartButtons();
    initializeViewButtons();
    updateCartCount();
});

// Category Filter Functionality
function initializeCategoryFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const productCards = document.querySelectorAll('.product-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            const category = this.getAttribute('data-category');
            
            // Filter products
            productCards.forEach(card => {
                if (category === 'all') {
                    card.classList.remove('hidden');
                } else {
                    const productCategory = card.getAttribute('data-category');
                    if (productCategory === category) {
                        card.classList.remove('hidden');
                    } else {
                        card.classList.add('hidden');
                    }
                }
            });
        });
    });
}

// Size Selection Functionality
function initializeSizeSelection() {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach((card, index) => {
        const sizeButtons = card.querySelectorAll('.size-btn');
        const addToCartBtn = card.querySelector('.btn-add');
        const productId = addToCartBtn.getAttribute('data-product-id');
        
        // Initially disable add to cart button
        addToCartBtn.disabled = true;
        addToCartBtn.style.opacity = '0.5';
        
        sizeButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                // Remove selected class from all size buttons in this card
                sizeButtons.forEach(b => b.classList.remove('selected'));
                
                // Add selected class to clicked button
                this.classList.add('selected');
                
                // Store selected size
                const size = this.getAttribute('data-size');
                selectedSizes[productId] = size;
                
                // Enable add to cart button
                addToCartBtn.disabled = false;
                addToCartBtn.style.opacity = '1';
            });
        });
    });
}

// Add to Cart Functionality
function initializeCartButtons() {
    const addToCartButtons = document.querySelectorAll('.btn-add');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.disabled) {
                alert('Please select a size first!');
                return;
            }
            
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name');
            const productPrice = this.getAttribute('data-product-price');
            const selectedSize = selectedSizes[productId];
            
            if (!selectedSize) {
                alert('Please select a size first!');
                return;
            }
            
            // Add to cart
            const cartItem = {
                id: productId,
                name: productName,
                price: parseFloat(productPrice),
                size: selectedSize,
                quantity: 1
            };
            
            // Check if item with same size already exists
            const existingItem = cart.find(item => 
                item.id === productId && item.size === selectedSize
            );
            
            if (existingItem) {
                existingItem.quantity++;
                alert(`${productName} (Size: ${selectedSize}) quantity updated in cart!`);
            } else {
                cart.push(cartItem);
                alert(`${productName} (Size: ${selectedSize}) added to cart!`);
            }
            
            updateCartCount();
            
            // Visual feedback
            this.textContent = 'Added!';
            this.style.background = '#4caf50';
            setTimeout(() => {
                this.textContent = 'Add to Cart';
                this.style.background = '#667eea';
            }, 1500);
        });
    });
}

// View Details Functionality
function initializeViewButtons() {
    const viewButtons = document.querySelectorAll('.btn-view');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            alert(`View details for product ID: ${productId}\n\nThis would typically open a product detail page or modal.`);
            // You can implement your own view details logic here
            // For example, open a modal or navigate to a detail page
        });
    });
}

// Update Cart Count
function updateCartCount() {
    const cartCount = document.getElementById('cart-count');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
}

// Helper function to get cart contents (useful for checkout)
function getCart() {
    return cart;
}

// Helper function to calculate cart total
function getCartTotal() {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0).toFixed(2);
}

// Helper function to clear cart
function clearCart() {
    cart = [];
    selectedSizes = {};
    updateCartCount();
}

// Console log for debugging (you can view cart in browser console)
console.log('Store initialized. Use getCart() to view cart contents.');
console.log('Use getCartTotal() to see total price.');
console.log('Use clearCart() to clear the cart.');