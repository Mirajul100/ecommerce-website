document.addEventListener('DOMContentLoaded', function () {

    // SweetAlert delete confirmation
    const deleteButtons = document.querySelectorAll('.sc-remove-btn');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const url = this.dataset.url;

            Swal.fire({
                title: 'Are you sure ?',
                text: "Do you really want to remove this product from your cart?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: 'rgba(213, 67, 67, 1)',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'Cancel',
                background: '#f0f0f0',
                color: '#333'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = url;
                }
            })
        });
    });

    // Close button for alert box
    document.addEventListener("click", function(e){
        const btn = e.target.closest('.btn-close');
        if (btn) {
            btn.parentElement.style.display = "none";
        }
    });

});

setTimeout(function(){
    $('#message').fadeOut('slow')
}, 3000)