document.getElementById("year").textContent = new Date().getFullYear();

const toggle = document.querySelector(".nav-toggle");
const links = document.querySelector(".nav-links");

if (toggle && links) {
  toggle.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
  });

  links.querySelectorAll("a").forEach((a) => {
    a.addEventListener("click", () => {
      links.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

const header = document.querySelector(".header");
let lastY = 0;

window.addEventListener("scroll", () => {
  const y = window.scrollY;
  if (header) {
    header.style.transform = y > lastY && y > 80 ? "translateY(-100%)" : "translateY(0)";
  }
  lastY = y;
}, { passive: true });
