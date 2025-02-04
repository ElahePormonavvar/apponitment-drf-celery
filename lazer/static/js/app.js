//setup nav
const navBtn = document.getElementById("nav-btn");
const navbar = document.getElementById("navbar");
const navClose = document.getElementById("nav-close");
//show nav
navBtn.addEventListener("click", () => {
    navbar.classList.add("show-nav");
});

navClose.addEventListener("click", () => {
    navbar.classList.remove("show-nav");
});