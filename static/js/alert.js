document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.sc-remove-btn');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const url = this.dataset.url;

            Swal.fire({
                title: 'Are you sure ?',
                text: "Do you really want to remove this product from your cart ?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: 'rgba(213, 67, 67, 1)',    // Red button
                cancelButtonColor: '#3085d6',  // Blue cancel
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'Cancel',
                background: '#f0f0f0',         // Popup background
                color: '#333',                  // Text color
                iconColor: '#e74c3c',           // Icon color
                customClass: {
                    popup: 'shadow-lg rounded-lg p-4'  // extra styling using Tailwind classes
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    // Redirect to Django delete URL
                    window.location.href = url;
                }
            })
        });
    });
});
