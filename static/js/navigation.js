document.addEventListener("DOMContentLoaded", function () {
  console.log("hello");
  const navToggle = document.querySelector(".nav-toggle");
  const navList = document.querySelector(".nav__list");
  const closeButton = document.querySelector(".nav-close");

  navToggle.addEventListener("click", function () {
    navList.classList.add("mobile-open");
  });

  closeButton.addEventListener("click", function () {
    navList.classList.remove("mobile-open");
  });
});
