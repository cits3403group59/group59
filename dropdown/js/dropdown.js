document.querySelectorAll('.dropdown').forEach(dropdown => {
  const btn = dropdown.querySelector('a');
  const menu = dropdown.querySelector('.dropdown-content');
//.open class manages "click" switching
//mouseleave manages "automatically retracting after moving out"
  btn.addEventListener('click', e => {
    e.preventDefault();
    dropdown.classList.toggle('open');
  });

  dropdown.addEventListener('mouseleave', () => {
    dropdown.classList.remove('open');
  });
});