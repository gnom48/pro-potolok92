const modal = document.getElementById("modal");
const closeModal = document.getElementById("closeModal");

document.querySelectorAll(".btn-order, .btn-primary, .order-btn").forEach((btn) => {
  btn.addEventListener("click", (event) => {
    if (btn.getAttribute("href") === "#") {
      event.preventDefault();
    }
    modal.style.display = "flex";
  });
});

closeModal.onclick = () => {
  modal.style.display = "none";
};

window.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});

(() => {
  const today = new Date().toISOString().slice(0, 10);
  const storageKey = "proPotolokVisitDate";

  if (localStorage.getItem(storageKey) === today) {
    return;
  }

  fetch("/api/visit", {
    method: "POST",
    credentials: "same-origin",
    keepalive: true
  }).then(() => {
    localStorage.setItem(storageKey, today);
  }).catch(() => {});
})();
