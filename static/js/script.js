const faders = document.querySelectorAll('.fade-up');

const appearOptions = {
  threshold: 0.3,
};

const appearOnScroll = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('show');
    observer.unobserve(entry.target);
  });
}, appearOptions);

faders.forEach(fader => {
  appearOnScroll.observe(fader);
});

// Меню бургер (как у тебя)
const burger = document.querySelector('.burger');
const nav = document.querySelector('nav');

burger.addEventListener('click', () => {
  nav.classList.toggle('active');
});


if (window.gsap && window.ScrollTrigger) {
  gsap.registerPlugin(ScrollTrigger);

  gsap.fromTo(".overlay-img",
    {
      opacity: 0,
      scale: 0.8,
      rotation: 0
    },
    {
      scrollTrigger: {
        trigger: ".overlay-img",
        start: "top 80%",
        once: true
      },
      opacity: 1,
      scale: 1,
      rotation: 720,
      duration: 2.5,
      ease: "power4.out"
    }
  );

  gsap.to(".overlay-img", {
    scrollTrigger: {
      trigger: ".overlay-img",
      start: "top 80%",
      once: true
    },
    y: -15,
    duration: 0.5,
    delay: 2.5,
    ease: "bounce.out"
  });
}


