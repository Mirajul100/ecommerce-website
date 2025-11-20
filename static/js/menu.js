const hamburger = document.getElementById("hamburger");
    const sideMenu = document.getElementById("sideMenu");
    const overlay = document.getElementById("overlay");

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("active");
        sideMenu.classList.toggle("active");
        overlay.classList.toggle("show");
    });

    overlay.addEventListener("click", () => {
        hamburger.classList.remove("active");
        sideMenu.classList.remove("active");
        overlay.classList.remove("show");
    });