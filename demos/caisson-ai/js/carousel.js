(() => {
  const carousels = document.querySelectorAll("[data-carousel]");
  if (!carousels.length) return;

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const AUTO_MS = 7000;

  carousels.forEach((root) => {
    const track = root.querySelector(".carousel-track");
    const slides = [...root.querySelectorAll(".carousel-slide")];
    const prev = root.querySelector("[data-carousel-prev]");
    const next = root.querySelector("[data-carousel-next]");
    const dotsHost = root.querySelector("[data-carousel-dots]");
    const label = root.querySelector("[data-carousel-label]");
    const count = root.querySelector("[data-carousel-count]");
    const progressBar = root.querySelector("[data-carousel-progress]");
    if (!track || slides.length === 0) return;

    let index = 0;
    let timer;
    let progressTimer;
    let progressStart;

    const pad = (n) => String(n).padStart(2, "0");

    const dots = slides.map((_, i) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = "carousel-dot";
      dot.setAttribute("aria-label", `Go to slide ${i + 1}`);
      dot.addEventListener("click", () => go(i));
      dotsHost?.appendChild(dot);
      return dot;
    });

    const updateMeta = () => {
      const slide = slides[index];
      const title = slide?.dataset.slideTitle || slide?.querySelector("h3")?.textContent || "";
      if (label) label.textContent = title;
      if (count) count.textContent = `${pad(index + 1)} / ${pad(slides.length)}`;
    };

    const resetProgress = () => {
      if (!progressBar) return;
      progressBar.style.transition = "none";
      progressBar.style.width = "0%";
      progressStart = performance.now();
      clearInterval(progressTimer);
      if (reduced || slides.length < 2) return;
      progressTimer = setInterval(() => {
        const elapsed = performance.now() - progressStart;
        const pct = Math.min((elapsed / AUTO_MS) * 100, 100);
        progressBar.style.width = `${pct}%`;
        if (pct >= 100) clearInterval(progressTimer);
      }, 50);
    };

    const go = (i) => {
      index = (i + slides.length) % slides.length;
      track.style.transform = `translateX(-${index * 100}%)`;
      dots.forEach((d, n) => d.classList.toggle("is-active", n === index));
      updateMeta();
      resetProgress();
      autoplay();
    };

    prev?.addEventListener("click", () => go(index - 1));
    next?.addEventListener("click", () => go(index + 1));

    root.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") go(index - 1);
      if (e.key === "ArrowRight") go(index + 1);
    });

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
      timer = setInterval(() => go(index + 1), AUTO_MS);
    };

    root.addEventListener("mouseenter", () => {
      clearInterval(timer);
      clearInterval(progressTimer);
      if (progressBar) progressBar.style.width = `${((performance.now() - progressStart) / AUTO_MS) * 100}%`;
    });
    root.addEventListener("mouseleave", () => {
      resetProgress();
      autoplay();
    });

    root.setAttribute("tabindex", "0");

    go(0);
  });
})();
