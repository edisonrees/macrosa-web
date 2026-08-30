(() => {
  const carousels = document.querySelectorAll("[data-carousel]");
  if (!carousels.length) return;

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  carousels.forEach((root) => {
    const track = root.querySelector(".carousel-track");
    const slides = [...root.querySelectorAll(".carousel-slide")];
    const prev = root.querySelector("[data-carousel-prev]");
    const next = root.querySelector("[data-carousel-next]");
    const dotsHost = root.querySelector("[data-carousel-dots]");
    if (!track || slides.length === 0) return;

    let index = 0;
    let timer;

    const dots = slides.map((_, i) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = "carousel-dot";
      dot.setAttribute("aria-label", `Go to slide ${i + 1}`);
      dot.addEventListener("click", () => go(i));
      dotsHost?.appendChild(dot);
      return dot;
    });

    const go = (i) => {
      index = (i + slides.length) % slides.length;
      track.style.transform = `translateX(-${index * 100}%)`;
      dots.forEach((d, n) => d.classList.toggle("is-active", n === index));
    };

    prev?.addEventListener("click", () => go(index - 1));
    next?.addEventListener("click", () => go(index + 1));

    let startX = 0;
    track.addEventListener(
      "touchstart",
      (e) => {
        startX = e.touches[0].clientX;
      },
      { passive: true }
    );
    track.addEventListener(
      "touchend",
      (e) => {
        const dx = e.changedTouches[0].clientX - startX;
        if (Math.abs(dx) < 40) return;
        go(dx > 0 ? index - 1 : index + 1);
      },
      { passive: true }
    );

    const autoplay = () => {
      if (reduced || slides.length < 2) return;
      clearInterval(timer);
      timer = setInterval(() => go(index + 1), 6000);
    };

    root.addEventListener("mouseenter", () => clearInterval(timer));
    root.addEventListener("mouseleave", autoplay);

    go(0);
    autoplay();
  });
})();
