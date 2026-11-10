'use strict';

function closeMobileMenu() {
  document.body.classList.remove('menu-open');
  document.querySelector('#mobileMenu').setAttribute('aria-expanded', 'false');
}

function renderMobileNavigation() {
  const destinations = [['home', '首页'], ['reading', '阅读'], ['listening', '听力'], ['words', '生词']];
  document.querySelector('#mobileNav').innerHTML = destinations.map(([id, label]) =>
    `<button data-mobile-route="${id}" ${route === id ? 'aria-current="page"' : ''}>${icon(id)}<span>${label}</span></button>`
  ).join('');
  document.querySelectorAll('[data-mobile-route]').forEach(button => {
    button.onclick = () => navigate(button.dataset.mobileRoute);
  });
  closeMobileMenu();
}

document.querySelector('#mobileMenu').onclick = () => {
  const open = document.body.classList.toggle('menu-open');
  document.querySelector('#mobileMenu').setAttribute('aria-expanded', String(open));
};
document.querySelector('#menuBackdrop').onclick = closeMobileMenu;

window.androidBack = () => {
  if (document.querySelector('#searchDialog').open) {
    document.querySelector('#searchDialog').close();
  } else if (document.body.classList.contains('menu-open')) {
    closeMobileMenu();
  } else if (current) {
    navigate(route);
  } else if (route !== 'home') {
    navigate('home');
  } else {
    return false;
  }
  return true;
};
