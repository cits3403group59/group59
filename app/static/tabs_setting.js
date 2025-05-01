function switchToTab(tabName) {
  document.querySelectorAll('main section').forEach(section => {
    section.classList.add('hidden');
  });
  const activeSection = document.getElementById(tabName);
  if (activeSection) {
    activeSection.classList.remove('hidden');
  }


   document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('bg-gray-300', 'font-bold');
    btn.classList.add('hover:bg-gray-300');
  });
   const activeBtn = document.querySelector(`.tab-btn[data-tab="${tabName}"]`);
     if (activeBtn) {
      activeBtn.classList.add('bg-gray-300', 'font-bold');
      activeBtn.classList.remove('hover:bg-gray-300');
  }
}

function initTabSwitching() {
  // left button to switch
  document.querySelectorAll('.tab-btn').forEach(button => {
    button.addEventListener('click', event => {
      event.preventDefault();
      const targetTab = button.getAttribute('data-tab');
      window.location.hash = targetTab;
      switchToTab(targetTab);
    });
  });

  const initialTab = window.location.hash.replace('#', '') || 'account';
  switchToTab(initialTab);
// Update the URL hash when the page loads
  window.addEventListener('hashchange', () => {
    const newTab = window.location.hash.replace('#', '') || 'account';
    switchToTab(newTab);
  });
}

window.addEventListener('DOMContentLoaded', initTabSwitching);