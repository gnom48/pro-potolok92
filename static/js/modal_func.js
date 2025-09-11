const modal = document.getElementById("modal");
const closeModal = document.getElementById("closeModal");
const form = document.getElementById("requestForm");
const phoneInput = document.getElementById("phoneInput");

// Открытие/закрытие
document.querySelectorAll(".btn-order, .btn-primary, .order-btn").forEach(btn => {
  btn.addEventListener("click", () => modal.style.display = "flex");
});
closeModal.onclick = () => modal.style.display = "none";
window.onclick = e => { if (e.target === modal) modal.style.display = "none"; };

// ===== Маска для телефона =====
function formatPhone(value) {
  let input = value.replace(/\D/g, ""); // только цифры

  if (input === "") return "";

  if (!input.startsWith("7")) input = "7" + input;
  input = input.substring(0, 11);

  let formatted = "+7";

  if (input.length > 1) {
    formatted += " (" + input.substring(1, Math.min(4, input.length));
  }
  if (input.length >= 4) {
    formatted += ")";
    if (input.length > 4) {
      formatted += " " + input.substring(4, Math.min(7, input.length));
    }
  }
  if (input.length >= 7) {
    formatted += "-" + input.substring(7, Math.min(9, input.length));
  }
  if (input.length >= 9) {
    formatted += "-" + input.substring(9, Math.min(11, input.length));
  }

  return formatted;
}

// Форматирование при вводе
phoneInput.addEventListener("input", () => {
  phoneInput.value = formatPhone(phoneInput.value);
});

// Backspace — удаляем последнюю цифру
phoneInput.addEventListener("keydown", (e) => {
  if (e.key === "Backspace") {
    let digits = phoneInput.value.replace(/\D/g, "");
    digits = digits.substring(0, digits.length - 1);
    phoneInput.value = formatPhone(digits);
    e.preventDefault();
  }
});

// ===== Отправка в Telegram =====
form.addEventListener("submit", function(e) {
  e.preventDefault();

  const name = form.name.value.trim();
  const phone = phoneInput.value.trim();

  if (name.length < 2) {
    alert("Введите корректное имя");
    return;
  }
  if (phone.length < 18) { // +7 (xxx) xxx-xx-xx = 18 символов
    alert("Введите корректный номер телефона");
    return;
  }

  const token = "8348692489:AAEI3a8VJaNlMI4YDPAFE0kWNmmn7YUN5mM"; // <-- сюда твой токен
  const chatId = "5921894758"; // <-- сюда chat_id
  const message = `📩 Новая заявка:\n👤 Имя: ${name}\n📞 Телефон: ${phone}`;

  fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text: message })
  })
    .then(() => {
      alert("Заявка успешно отправлена!");
      modal.style.display = "none";
      form.reset();
    })
    .catch(() => alert("Ошибка при отправке"));
});
