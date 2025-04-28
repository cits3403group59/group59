const tabs  = document.querySelectorAll('.tab-btn');
const panes = document.querySelectorAll('main section');

tabs.forEach(btn => {
  btn.addEventListener('click', () => {
    tabs.forEach(b => b.classList.remove('bg-gray-300'));
    btn.classList.add('bg-gray-300');
    const target = btn.dataset.tab;
    panes.forEach(sec => {
      sec.id === target
        ? sec.classList.remove('hidden')
        : sec.classList.add('hidden');
    });
  });
});

