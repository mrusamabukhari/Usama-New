// ===== NAVBAR MOBILE TOGGLE =====
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
    navLinks.style.flexDirection = 'column';
    navLinks.style.position = 'absolute';
    navLinks.style.top = '70px';
    navLinks.style.right = '24px';
    navLinks.style.background = '#fff';
    navLinks.style.padding = '16px 24px';
    navLinks.style.borderRadius = '12px';
    navLinks.style.boxShadow = '0 8px 24px rgba(0,0,0,0.12)';
  });
}

// ===== CONTACT FORM — Opens WhatsApp with pre-filled message =====
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const name = this.querySelector('input[type="text"]').value;
    const phone = this.querySelector('input[type="tel"]').value;
    const employment = this.querySelector('select').value;
    const pkg = this.querySelectorAll('select')[1].value;
    const msg = this.querySelector('textarea').value;

    const waMessage = encodeURIComponent(
      `Hi TaxEase Pakistan! I want to file my income tax return.\n\n` +
      `Name: ${name}\n` +
      `Phone: ${phone}\n` +
      `Employment Type: ${employment}\n` +
      `Package: ${pkg || 'Not selected yet'}\n` +
      `Message: ${msg || 'None'}\n\n` +
      `Please guide me on the next steps.`
    );

    // Replace with your actual WhatsApp number
    window.open(`https://wa.me/923000000000?text=${waMessage}`, '_blank');
  });
}

// ===== SMOOTH SCROLL for anchor links =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // Close mobile menu if open
      if (navLinks) navLinks.style.display = '';
    }
  });
});

// ===== SCROLL ANIMATIONS =====
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.card, .service-card, .pricing-card, .step, .testimonial-card, .faq-item').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

// ===== ACTIVE NAV HIGHLIGHT =====
const sections = document.querySelectorAll('section[id]');
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(section => {
    if (window.scrollY >= section.offsetTop - 100) current = section.id;
  });
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.style.color = link.getAttribute('href') === `#${current}` ? 'var(--green)' : '';
  });
});
