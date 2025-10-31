document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll('.size-btn');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
        });
    });
});

