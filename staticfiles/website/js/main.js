const toggle = document.getElementById("themeToggle");

toggle.addEventListener("click", () => {

    const dark = document.documentElement.dataset.theme === "dark";

    document.documentElement.dataset.theme = dark
        ? "light"
        : "dark";

    localStorage.setItem(
        "theme",
        dark ? "light" : "dark"
    );

    toggle.textContent = dark ? "🌙" : "☀️";
});


const savedTheme = localStorage.getItem("theme");

if (savedTheme) {
    document.documentElement.dataset.theme = savedTheme;
    toggle.textContent =
        savedTheme === "dark" ? "☀️" : "🌙";
}



const menuBtn =
        document.getElementById("menuBtn");

    const mobileMenu =
        document.getElementById("mobileMenu");

    const mobileClose =
        document.getElementById("mobileClose");

    const mobileOverlay =
        document.getElementById("mobileOverlay");


    function openMenu() {

        mobileMenu.classList.add("active");

        mobileOverlay.classList.add("active");

        document.body.style.overflow = "hidden";
    }


    function closeMenu() {

        mobileMenu.classList.remove("active");

        mobileOverlay.classList.remove("active");

        document.body.style.overflow = "";
    }


    menuBtn.addEventListener("click", openMenu);

    mobileClose.addEventListener("click", closeMenu);

    mobileOverlay.addEventListener("click", closeMenu);


    /* Close with ESC */

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {
            closeMenu();
        }

    });


    var swiper = new Swiper('.mySwiper', {
        spaceBetween: 30,
        pagination: {
          el: '.swiper-pagination',
          clickable: true,
        },
      });