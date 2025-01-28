document.addEventListener("DOMContentLoaded", function () {
  const navToggle = document.querySelector(".nav-toggle");
  const navList = document.querySelector(".nav__list");
  const closeButton = document.querySelector(".nav-close");

  navToggle.addEventListener("click", function () {
    navList.classList.add("mobile-open");
    closeButton.style.display = "block";
    closeButton.style.color = "var(--neutral-200)";
    closeButton.style.zIndex = "100";
  });

  closeButton.addEventListener("click", function () {
    navList.classList.remove("mobile-open");
  });
});
