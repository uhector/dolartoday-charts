const menuButton = document.getElementById('menu-button');
const menuItems = document.getElementById('menu-items');

menuButton.addEventListener('click', () => {
    menuItems.classList.toggle('show');
    menuButton.classList.toggle('activate')   
});