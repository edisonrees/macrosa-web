(() => {
  const header = document.querySelector(".site-header");
  const onScroll = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  document.querySelectorAll("[data-img]").forEach((img) => {
    const wrap = img.closest(".img-load");
    const done = () => wrap?.classList.add("is-loaded");
    if (img.complete && img.naturalWidth > 0) {
      done();
    } else {
      img.addEventListener("load", done, { once: true });
      img.addEventListener("error", done, { once: true });
    }
  });

  const reveals = document.querySelectorAll(".reveal");
  if (reveals.length) {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      reveals.forEach((el) => el.classList.add("is-in"));
    } else {
      const io = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (!entry.isIntersecting) continue;
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        },
        { threshold: 0.12, rootMargin: "0px 0px -5% 0px" }
      );
      reveals.forEach((el, i) => {
        el.style.transitionDelay = `${Math.min(i * 0.04, 0.2)}s`;
        io.observe(el);
      });
    }
  }

  const dockLinks = document.querySelectorAll(".mobile-dock a[href^='#']");
  if (dockLinks.length) {
    const sections = [...dockLinks]
      .map((a) => document.querySelector(a.getAttribute("href")))
      .filter(Boolean);
    const spy = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          const id = `#${entry.target.id}`;
          dockLinks.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === id));
        }
      },
      { rootMargin: "-40% 0px -50% 0px", threshold: 0 }
    );
    sections.forEach((s) => spy.observe(s));
  }
})();
