const prices = {
    ceilingType: {
        classic: 600,
        floating: 1200,
        shadow: 800
    },
    materialType: {
        glossy: 0,
        matte: 0,
        satin: 0
    },
    elements: {
        lamps: 400,
        track: 400,
        chandelier: 300,
        lightLine: 2500
    }
};

// Получаем элементы
const areaInput = document.getElementById('area');
const areaValue = document.getElementById('areaValue');
const priceMinEl = document.getElementById('priceMin');
const priceMaxEl = document.getElementById('priceMax');

// Обновление значения площади
areaInput.addEventListener('input', () => {
    areaValue.textContent = areaInput.value;
    calculatePrice();
});

// Кнопки +/-
document.querySelectorAll('.plus, .minus').forEach(btn => {
    btn.addEventListener('click', () => {
        const targetId = btn.dataset.target;
        const span = document.getElementById(targetId);
        let value = parseInt(span.textContent);
        if (btn.classList.contains('plus')) {
            value++;
        } else if (btn.classList.contains('minus') && value > 0) {
            value--;
        }
        span.textContent = value;
        calculatePrice();
    });
});

// Радио-кнопки
document.querySelectorAll('input[type=radio]').forEach(radio => {
    radio.addEventListener('change', calculatePrice);
});

function calculatePrice() {
    const ceilingType = document.querySelector('input[name="ceilingType"]:checked').value;
    const materialType = document.querySelector('input[name="materialType"]:checked').value;
    const area = parseInt(areaInput.value);

    let total = (area * (prices.ceilingType[ceilingType] + prices.materialType[materialType]));

    Object.keys(prices.elements).forEach(el => {
        const count = parseInt(document.getElementById(el).textContent);
        total += count * prices.elements[el];
    });

    priceMinEl.textContent = total.toLocaleString();
    priceMaxEl.textContent = Math.round(total * 1.15).toLocaleString();
}

// Стартовый расчёт
calculatePrice();


gsap.registerPlugin(ScrollTrigger);

// Анимация всех блоков калькулятора
gsap.from(".calc-block", {
  y: 50,           // подлетаем снизу
  opacity: 0,       // появляемся
  scale: 0.95,      // чуть уменьшаемся при старте
  stagger: 0.2,     // последовательное появление блоков
  duration: 0.8,
  ease: "power2.out",
  scrollTrigger: {
    trigger: ".calc-container",
    start: "top 90%",     // когда контейнер почти виден
    end: "bottom top",    // пока нижняя граница контейнера дойдет до верха экрана
    scrub: 1.2,           // плавная привязка к скроллу
    // pin: false, чтобы не увеличивать пространство
    toggleActions: "play reverse play reverse" // повторная анимация при скролле вверх
  }
});

