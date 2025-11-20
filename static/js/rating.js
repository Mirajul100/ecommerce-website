let selectedRating = 0;
const stars = document.querySelectorAll('.star');
const ratingText = document.getElementById('ratingText');
const reviewForm = document.getElementById('reviewForm');
const reviewInput = document.getElementById('reviewInput');
const reviewsList = document.getElementById('reviewsList');

const ratingMessages = {
    1: "Poor - Not satisfied",
    2: "Fair - Below expectations",
    3: "Good - Meets expectations",
    4: "Very Good - Exceeds expectations",
    5: "Excellent - Outstanding!"
};

stars.forEach(star => {
    star.addEventListener('click', function() {
        selectedRating = parseInt(this.getAttribute('data-rating'));
        updateStars();
        ratingText.textContent = ratingMessages[selectedRating];
    });

    star.addEventListener('mouseenter', function() {
        const hoverRating = parseInt(this.getAttribute('data-rating'));
        highlightStars(hoverRating);
    });
});

document.getElementById('starRating').addEventListener('mouseleave', function() {
    updateStars();
});

function highlightStars(rating) {
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

function updateStars() {
    highlightStars(selectedRating);
}

reviewForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (selectedRating === 0) {
        alert('Please select a rating before submitting!');
        return;
    }

    const reviewText = reviewInput.value.trim();
    if (!reviewText) {
        alert('Please write a review!');
        return;
    }

    addReview(selectedRating, reviewText);
    
    selectedRating = 0;
    reviewInput.value = '';
    updateStars();
    ratingText.textContent = 'Click to rate';
    
    alert('Thank you for your review!');
});

function addReview(rating, text) {
    const reviewItem = document.createElement('div');
    reviewItem.className = 'review-item';
    
    const starString = '★'.repeat(rating) + '☆'.repeat(5 - rating);
    
    reviewItem.innerHTML = `
        <div class="review-header">
            <div class="review-stars">${starString}</div>
            <div class="review-date">Just now</div>
        </div>
        <div class="review-text">${text}</div>
    `;
    
    reviewsList.insertBefore(reviewItem, reviewsList.children[1]);
}