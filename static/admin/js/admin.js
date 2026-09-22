document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.querySelector(".sidebar");

    const sidebarToggle = document.querySelector(".sidebar-toggle");

    const sidebarOverlay = document.querySelector(".sidebar-overlay");


    // Open / Close Sidebar

    if (sidebarToggle) {

        sidebarToggle.addEventListener("click", function () {

            sidebar.classList.toggle("active");

            sidebarOverlay.classList.toggle("active");

        });

    }


    // Close Sidebar When Clicking Overlay

    if (sidebarOverlay) {

        sidebarOverlay.addEventListener("click", function () {

            sidebar.classList.remove("active");

            sidebarOverlay.classList.remove("active");

        });

    }


    // Close Sidebar When Screen Changes To Desktop

    window.addEventListener("resize", function () {

        if (window.innerWidth > 991) {

            sidebar.classList.remove("active");

            sidebarOverlay.classList.remove("active");

        }

    });

});