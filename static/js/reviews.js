const wrapper = document.querySelector('.reviews-wrapper');
const cards = document.querySelectorAll('.review-card');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');

let index = 0;
const visibleCards = 3;

function updateCarousel() {
  wrapper.style.transform = `translateX(${-index * (cards[0].offsetWidth + 20)}px)`;

  // При каждом листании убеждаемся, что все карточки видимы
  cards.forEach(card => {
    if (window.gsap) {
      gsap.to(card, { opacity: 1, x: 0, y: 0, duration: 0.3, overwrite: true });
    } else {
      card.style.opacity = 1;
      card.style.transform = "translate(0, 0)";
    }
  });
}

nextBtn.addEventListener('click', () => {
  if (index < cards.length - visibleCards) {
    index++;
    updateCarousel();
  }
});

prevBtn.addEventListener('click', () => {
  if (index > 0) {
    index--;
    updateCarousel();
  }
});

if (window.gsap && window.ScrollTrigger) {
  gsap.registerPlugin(ScrollTrigger);

  gsap.from(".review-card:nth-child(-n+3)", {
    x: -100,
    y: 30,
    opacity: 0,
    stagger: 0.4,
    duration: 0.8,
    ease: "power2.out",
    scrollTrigger: {
      trigger: ".reviews-section",
      start: "top 80%",
      end: "bottom 20%",
      toggleActions: "play none none reverse"
    }
  });

  gsap.set(".review-card:nth-child(n+4)", {opacity: 1, x: 0, y: 0});
}
