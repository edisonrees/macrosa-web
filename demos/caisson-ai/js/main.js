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
        { threshold: 0.1, rootMargin: "0px 0px -4% 0px" }
      );
      reveals.forEach((el, i) => {
        el.style.transitionDelay = `${Math.min(i * 0.05, 0.25)}s`;
        io.observe(el);
      });
    }
  }

  const sectionLinks = [
    ...document.querySelectorAll(".nav a[href^='#']"),
    ...document.querySelectorAll(".mobile-dock a[href^='#']"),
  ];
  if (sectionLinks.length) {
    const sections = [...new Set(sectionLinks.map((a) => a.getAttribute("href")))]
      .map((id) => document.querySelector(id))
      .filter(Boolean);
    const spy = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          const id = `#${entry.target.id}`;
          sectionLinks.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === id));
        }
      },
      { rootMargin: "-35% 0px -55% 0px", threshold: 0 }
    );
    sections.forEach((s) => spy.observe(s));
  }
})();
