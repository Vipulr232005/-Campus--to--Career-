/**
 * HireSense AI — Scroll reveal, mobile menu
 */
(function() {
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) e.target.classList.add('visible');
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
  document.querySelectorAll('.reveal').forEach(function(el) { obs.observe(el); });

  var toggle = document.querySelector('.navbar-toggle');
  var links = document.querySelector('.navbar-links');
  if (toggle && links) {
    toggle.addEventListener('click', function() { links.classList.toggle('open'); });
  }

  var sidebarToggle = document.querySelector('.sidebar-toggle');
  var sidebar = document.querySelector('.dashboard-sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function() { sidebar.classList.toggle('open'); });
  }
})();
