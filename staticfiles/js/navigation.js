document.addEventListener("DOMContentLoaded", function () {
  const navToggle = document.querySelector(".nav-toggle");
  const navList = document.querySelector(".nav__list");
  const closeButton = document.querySelector(".nav-close");

  navToggle.addEventListener("click", function () {
    console.log("click");
    navList.classList.add("mobile-open");
    closeButton.style.display = "block";
  });

  closeButton.addEventListener("click", function () {
    navList.classList.remove("mobile-open");
    closeButton.style.display = "none";
  });
});
