// Please see documentation at https://learn.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Add to cart functionality
$(document).ready(function () {
    // Enable AJAX add to cart
    $(document).on('submit', '.ajax-cart-form', function (e) {
        e.preventDefault();
        var form = $(this);
        
        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: form.serialize(),
            success: function (data) {
                if (data.success) {
                    // Update cart count
                    $('.cart-count').text(data.cartCount);
                    
                    // Show success message
                    alert(data.message);
                }
            },
            error: function () {
                alert('Error adding product to cart. Please try again.');
            }
        });
    });
});
