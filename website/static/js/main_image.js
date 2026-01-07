$(document).ready(function() {
    
    // Thumbnail click handler
    $('.thumb a').on('click', function(e) {
        e.preventDefault();
        
        // Get image URL
        var newImageUrl = $(this).attr('href');
        $('.thumb a').removeClass('active');
        $(this).addClass('active');
        
        $('.single-product-img').fadeOut(300, function() {
            $(this).attr('src', newImageUrl);
            $(this).fadeIn(300);
        });
    });
    $('.thumb a:first').addClass('active');
});