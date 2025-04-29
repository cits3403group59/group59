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

document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById('menu-toggle'); // Button to open the side menu
  const closeBtn = document.getElementById('menu-close'); // Button to close the side menu
  const sideMenu = document.getElementById('side-menu'); // The side menu itself

  if (toggleBtn && closeBtn && sideMenu) {
      // Open the side menu
      toggleBtn.addEventListener('click', () => {
          sideMenu.classList.remove('-translate-x-full'); // Remove the class that hides the menu
          document.body.classList.add('overflow-hidden'); // Prevent scrolling on the body
      });

      // Close the side menu
      closeBtn.addEventListener('click', () => {
          sideMenu.classList.add('-translate-x-full'); // Add the class that hides the menu
          document.body.classList.remove('overflow-hidden'); // Allow scrolling on the body
      });
  }
});
