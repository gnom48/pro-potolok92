const track = document.querySelector('.carousel-track');
const slides = Array.from(track.children);
const nextButton = document.querySelector('.carousel-btn.next');
const prevButton = document.querySelector('.carousel-btn.prev');

let currentIndex = 0;

function updateCarousel() {
  const slideWidth = slides[0].getBoundingClientRect().width + 20; // margin-right = 20
  const amountToMove = slideWidth * currentIndex;
  track.style.transform = `translateX(-${amountToMove}px)`;
}

nextButton.addEventListener('click', () => {
  if (currentIndex < slides.length - 1) {
    currentIndex++;
    updateCarousel();
  }
});

prevButton.addEventListener('click', () => {
  if (currentIndex > 0) {
    currentIndex--;
    updateCarousel();
  }
});

// Swipe support for mobile
let startX = 0;
let isDragging = false;

track.addEventListener('touchstart', e => {
  startX = e.touches[0].clientX;
  isDragging = true;
});

track.addEventListener('touchmove', e => {
  if (!isDragging) return;
  const currentX = e.touches[0].clientX;
  const diffX = startX - currentX;

  if (diffX > 50 && currentIndex < slides.length - 1) {
    currentIndex++;
    updateCarousel();
    isDragging = false;
  } else if (diffX < -50 && currentIndex > 0) {
    currentIndex--;
    updateCarousel();
    isDragging = false;
  }
});

track.addEventListener('touchend', () => {
  isDragging = false;
});
