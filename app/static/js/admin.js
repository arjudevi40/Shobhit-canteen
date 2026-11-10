/**
 * Shobhit University Gangoh (SUG) - Canteen Management System
 * Admin Dashboard & Stock Operations JavaScript
 */

function toggleItemStock(itemId, checkboxElem) {
  fetch(`/api/toggle-availability/${itemId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        showToast(`"${itemId}" is now ${data.status_label}`, 'success');
        const labelElem = document.getElementById(`stock-label-${itemId}`);
        if (labelElem) {
          labelElem.textContent = data.status_label;
          labelElem.style.color = data.is_available ? 'var(--veg-green)' : 'var(--nonveg-red)';
        }
      } else {
        showToast('Error toggling availability', 'danger');
        checkboxElem.checked = !checkboxElem.checked;
      }
    })
    .catch(err => {
      console.error(err);
      showToast('Network error updating stock', 'danger');
      checkboxElem.checked = !checkboxElem.checked;
    });
}

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    const firstInput = modal.querySelector('input, select, textarea');
    if (firstInput) firstInput.focus();
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
}

// Close modal when clicking on backdrop or pressing ESC
window.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('open');
    e.target.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const openModals = document.querySelectorAll('.modal-overlay.open');
    openModals.forEach(m => {
      m.classList.remove('open');
      m.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    });
  }
});
