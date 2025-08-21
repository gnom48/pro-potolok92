const modal = document.getElementById("modal");
const closeModal = document.getElementById("closeModal");
const form = document.getElementById("requestForm");

// Получаем все кнопки с классами btn-order и btn-primary
const orderButtons = document.querySelectorAll(".btn-order, .btn-primary, .order-btn");

// Открытие модального окна при клике на любую из этих кнопок
orderButtons.forEach(button => {
    button.addEventListener("click", () => {
        modal.style.display = "flex";
    });
});

// Закрытие по крестику
closeModal.onclick = () => modal.style.display = "none";

// Закрытие при клике вне модального окна
window.onclick = (e) => { if (e.target === modal) modal.style.display = "none"; };

// ==== Telegram ====
form.addEventListener("submit", function(e) {
  e.preventDefault();

  const name = form.name.value;
  const phone = form.phone.value;

  const token = "8348692489:AAEI3a8VJaNlMI4YDPAFE0kWNmmn7YUN5mM"; 
  const chatId = "1115007593";   
  const message = `📩 Новая заявка:\n👤 Имя: ${name}\n📞 Телефон: ${phone}`;

  fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text: message })
  }).then(() => {
    alert("Заявка успешно отправлена!");
    modal.style.display = "none";
    form.reset();
  }).catch(() => alert("Ошибка при отправке"));
});
