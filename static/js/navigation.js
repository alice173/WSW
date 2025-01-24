document.addEventListener("DOMContentLoaded", function () {
  const navToggle = document.querySelector(".nav-toggle");
  const navList = document.querySelector(".nav__list");

  navToggle.addEventListener("click", function () {
    navList.classList.toggle("active");
  });
});
