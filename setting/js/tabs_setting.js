document.addEventListener('DOMContentLoaded', () => {
  const tabs   = document.querySelectorAll('.tab-btn');
  const panels = document.querySelectorAll('main section');

  tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      tabs.forEach(b => b.classList.remove('bg-gray-300'));
      btn.classList.add('bg-gray-300');
      const target = btn.dataset.tab;
      panels.forEach(sec => {
        sec.id === target
          ? sec.classList.remove('hidden')
          : sec.classList.add('hidden');
      });
    });
  });

  const h = location.hash.slice(1);
  if (h) {
    const btn = document.querySelector(`[data-tab="${h}"]`);
    if (btn) btn.click();
  }
});