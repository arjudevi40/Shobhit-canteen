/**
 * Shobhit University Gangoh (SUG) - Canteen Management System
 * Core Client-side Logic (Cart, Search, Live Order Polling, Toast, Accessibility)
 */

// Storage key for cart items
const CART_STORAGE_KEY = 'sug_canteen_cart_v1';

// Global Cart Utilities
const CanteenCart = {
  getItems() {
    try {
      const data = localStorage.getItem(CART_STORAGE_KEY);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.error('Error reading cart from localStorage', e);
      return [];
    }
  },

  saveItems(items) {
    try {
      localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items));
      this.updateNavbarBadge();
    } catch (e) {
      console.error('Error saving cart to localStorage', e);
    }
  },

  addItem(item, btnElement = null) {
    const items = this.getItems();
    const existing = items.find(i => i.item_id === item.item_id);

    if (existing) {
      existing.quantity += (item.quantity || 1);
    } else {
      items.push({
        item_id: item.item_id,
        name: item.name,
        price: parseFloat(item.price),
        image: item.image || '',
        quantity: item.quantity || 1
      });
    }

    this.saveItems(items);
    showToast(`Added "${item.name}" to tray!`, 'success');

    // Visual feedback on button if passed
    if (btnElement && btnElement.tagName === 'BUTTON') {
      const originalText = btnElement.innerHTML;
      btnElement.classList.add('btn-added');
      btnElement.innerHTML = '✓ Added!';
      setTimeout(() => {
        btnElement.classList.remove('btn-added');
        btnElement.innerHTML = originalText;
      }, 1200);
    }

    // Pulse cart badge
    const badge = document.getElementById('nav-cart-count');
    if (badge) {
      badge.style.transform = 'scale(1.25)';
      setTimeout(() => badge.style.transform = '', 250);
    }
  },

  updateQuantity(itemId, delta) {
    let items = this.getItems();
    const target = items.find(i => i.item_id === itemId);

    if (target) {
      target.quantity += delta;
      if (target.quantity <= 0) {
        items = items.filter(i => i.item_id !== itemId);
        showToast('Dish removed from tray', 'info');
      }
    }

    this.saveItems(items);
    if (typeof renderCartPage === 'function') {
      renderCartPage();
    }
  },

  removeItem(itemId) {
    let items = this.getItems();
    items = items.filter(i => i.item_id !== itemId);
    this.saveItems(items);
    showToast('Item removed from tray', 'info');
    if (typeof renderCartPage === 'function') {
      renderCartPage();
    }
  },

  clear() {
    localStorage.removeItem(CART_STORAGE_KEY);
    this.updateNavbarBadge();
  },

  getCount() {
    const items = this.getItems();
    return items.reduce((acc, i) => acc + (i.quantity || 1), 0);
  },

  getTotal() {
    const items = this.getItems();
    return items.reduce((acc, i) => acc + (i.price * (i.quantity || 1)), 0);
  },

  updateNavbarBadge() {
    const badges = document.querySelectorAll('#nav-cart-count, #mobile-cart-count');
    const count = this.getCount();
    badges.forEach(badge => {
      if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline-flex' : 'none';
      }
    });

    // Update bottom sticky tray bar if present
    if (typeof checkFloatingCart === 'function') {
      checkFloatingCart();
    }
  }
};

// Accessible Toast Notification System
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.setAttribute('role', 'status');
    container.setAttribute('aria-live', 'polite');
    document.body.appendChild(container);
  }

  const icons = {
    success: '✅',
    danger: '⚠️',
    info: 'ℹ️'
  };

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <div style="display: flex; align-items: center; gap: 8px;">
      <span>${icons[type] || 'ℹ️'}</span>
      <span>${message}</span>
    </div>
    <button type="button" onclick="this.parentElement.remove()" style="background: none; border: none; color: #cbd5e1; cursor: pointer; font-size: 1.1rem; line-height: 1; padding: 2px 6px;" aria-label="Close notification">&times;</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

// Quick Fill Demo Credentials on Login Page
function fillDemo(role) {
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');

  if (!emailInput || !passwordInput) return;

  if (role === 'admin') {
    emailInput.value = 'admin@shobhit.ac.in';
    passwordInput.value = 'admin123';
    showToast('Admin credentials filled (Prof. Chauhan)!', 'info');
  } else if (role === 'staff') {
    emailInput.value = 'staff@shobhit.ac.in';
    passwordInput.value = 'staff123';
    showToast('Faculty / Staff credentials filled (Dr. Verma)!', 'info');
  } else {
    emailInput.value = 'student@shobhit.ac.in';
    passwordInput.value = 'student123';
    showToast('Student credentials filled (Aman Sharma)!', 'info');
  }

  // Visual confirmation highlight
  [emailInput, passwordInput].forEach(inp => {
    inp.style.transition = 'background-color 0.3s ease';
    inp.style.backgroundColor = '#ecfdf5';
    setTimeout(() => inp.style.backgroundColor = '', 500);
  });
}

// Live Polling for Student Order Tracking
function initOrderPolling(token) {
  if (!token) return;

  const statusMap = {
    'Pending': 1,
    'Preparing': 2,
    'Ready': 3,
    'Delivered': 4,
    'Cancelled': 0
  };

  const statusDescMap = {
    'Pending': 'Your order has been queued at the canteen counter and is awaiting preparation.',
    'Preparing': '🍳 Chef is actively preparing your fresh hot food in the campus kitchen.',
    'Ready': '🎉 Your food is READY! Please show your Token at the pickup counter.',
    'Delivered': '✅ Order collected. Enjoy your fresh meal at Shobhit University!',
    'Cancelled': '❌ This order was cancelled.'
  };

  const checkStatus = () => {
    fetch(`/api/order-status/${token}`)
      .then(res => res.json())
      .then(data => {
        if (!data || data.error) return;

        const currentStatus = data.status;
        const stepNum = statusMap[currentStatus] || 1;

        // Update progress bar width
        const progressFill = document.getElementById('order-progress-fill');
        if (progressFill) {
          const percents = { 1: '0%', 2: '33%', 3: '66%', 4: '100%' };
          progressFill.style.width = percents[stepNum] || '0%';
        }

        // Update active/completed step classes
        for (let i = 1; i <= 4; i++) {
          const node = document.getElementById(`step-node-${i}`);
          if (node) {
            node.classList.remove('active', 'completed');
            if (i < stepNum) {
              node.classList.add('completed');
            } else if (i === stepNum) {
              node.classList.add('active');
            }
          }
        }

        // Update status text pill
        const statusPill = document.getElementById('order-current-status-pill');
        if (statusPill) {
          statusPill.textContent = currentStatus;
          statusPill.className = `status-badge status-${currentStatus.toLowerCase()}`;
        }

        const statusNote = document.getElementById('order-status-description');
        if (statusNote && statusDescMap[currentStatus]) {
          statusNote.innerHTML = statusDescMap[currentStatus];
        }

        // If completed or cancelled, stop polling
        if (currentStatus === 'Delivered' || currentStatus === 'Cancelled') {
          clearInterval(pollInterval);
        }
      })
      .catch(err => console.debug('Status poll error:', err));
  };

  // Poll every 4 seconds
  const pollInterval = setInterval(checkStatus, 4000);
}

// Copy Token Helper
function copyToken(tokenStr) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(tokenStr).then(() => {
      showToast(`Token #${tokenStr} copied to clipboard!`, 'success');
    }).catch(() => {
      showToast(`Token: ${tokenStr}`, 'info');
    });
  } else {
    showToast(`Token: ${tokenStr}`, 'info');
  }
}

// Mobile Navigation Toggle
function initMobileNav() {
  const toggleBtn = document.getElementById('mobile-menu-toggle');
  const drawer = document.getElementById('mobile-drawer');
  const overlay = document.getElementById('mobile-drawer-overlay');
  const closeBtn = document.getElementById('mobile-drawer-close');

  if (!toggleBtn || !drawer || !overlay) return;

  const openDrawer = () => {
    drawer.classList.add('active');
    overlay.classList.add('active');
    toggleBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  };

  const closeDrawer = () => {
    drawer.classList.remove('active');
    overlay.classList.remove('active');
    toggleBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  };

  toggleBtn.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  overlay.addEventListener('click', closeDrawer);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.classList.contains('active')) {
      closeDrawer();
    }
  });
}

// Instant Filter for Menu Page (Search + Veg toggle)
function initMenuFilters() {
  const searchInput = document.getElementById('menu-search-input');
  const foodCards = document.querySelectorAll('.food-card');
  const vegOnlyToggle = document.getElementById('filter-veg-only');

  function filterItems() {
    const q = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const vegOnly = vegOnlyToggle ? vegOnlyToggle.checked : false;

    let visibleCount = 0;

    foodCards.forEach(card => {
      const title = card.getAttribute('data-name')?.toLowerCase() || '';
      const cat = card.getAttribute('data-category')?.toLowerCase() || '';
      const desc = card.getAttribute('data-desc')?.toLowerCase() || '';
      const isVeg = card.getAttribute('data-veg') === 'true';

      const matchesSearch = !q || title.includes(q) || cat.includes(q) || desc.includes(q);
      const matchesVeg = !vegOnly || isVeg;

      if (matchesSearch && matchesVeg) {
        card.style.display = 'flex';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    // Handle no-items indicator
    const noResultsMsg = document.getElementById('no-search-results');
    if (noResultsMsg) {
      noResultsMsg.style.display = visibleCount === 0 ? 'block' : 'none';
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', filterItems);
  }
  if (vegOnlyToggle) {
    vegOnlyToggle.addEventListener('change', filterItems);
  }
}

// Document Ready
document.addEventListener('DOMContentLoaded', () => {
  CanteenCart.updateNavbarBadge();
  initMobileNav();
  initMenuFilters();
});
