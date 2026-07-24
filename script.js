/* ============================================
   24STANKI.RU — Main Script 2026
   Scroll animations, counters, nav, hamburger
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* === SCROLL REVEAL (Intersection Observer) === */
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger').forEach(el => {
    revealObserver.observe(el);
  });

  /* === ANIMATED COUNTERS === */
  function animateCounter(el, target, duration = 2000) {
    const start = performance.now();
    const suffix = el.dataset.suffix || '+';
    const update = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(eased * target);
      el.textContent = current.toLocaleString('ru-RU') + (progress >= 1 ? suffix : '');
      if (progress < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
  }

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const target = parseInt(entry.target.dataset.target, 10);
        if (target) animateCounter(entry.target, target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('[data-target]').forEach(el => {
    counterObserver.observe(el);
  });

  /* === STICKY NAV === */
  const nav = document.querySelector('.nav');
  if (nav) {
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
      const currentScroll = window.scrollY;
      if (currentScroll > 60) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
      lastScroll = currentScroll;
    }, { passive: true });
  }

  /* === HAMBURGER MENU === */
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.nav-mobile');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active');
      mobileMenu.classList.toggle('active');
      document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    });
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        mobileMenu.classList.remove('active');
        document.body.style.overflow = '';
      });
    });
  }

  /* === SMOOTH SCROLL for anchor links === */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* === PORTFOLIO FILTER === */
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioCards = document.querySelectorAll('.portfolio-card');
  if (filterBtns.length && portfolioCards.length) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        portfolioCards.forEach(card => {
          if (filter === 'all' || card.dataset.category === filter) {
            card.style.display = '';
            setTimeout(() => card.style.opacity = '1', 50);
          } else {
            card.style.opacity = '0';
            setTimeout(() => card.style.display = 'none', 300);
          }
        });
      });
    });
  }

  /* === VIDEO SOUND TOGGLE === */
  const soundBtn = document.getElementById('soundToggle');
  const heroVideo = document.getElementById('heroVideo');
  if (soundBtn && heroVideo) {
    soundBtn.addEventListener('click', () => {
      if (heroVideo.muted) {
        heroVideo.muted = false;
        heroVideo.volume = 0.5;
        soundBtn.textContent = '🔊 Выключить звук';
      } else {
        heroVideo.muted = true;
        soundBtn.textContent = '🔇 Включить звук';
      }
    });
  }

  /* === LAZY LOAD IMAGES === */
  document.querySelectorAll('img[loading="lazy"]').forEach(img => {
    if (img.complete) {
      img.classList.add('loaded');
    } else {
      img.addEventListener('load', () => img.classList.add('loaded'));
    }
  });

});
