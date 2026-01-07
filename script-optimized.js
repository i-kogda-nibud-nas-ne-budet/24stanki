// Оптимизированный JavaScript для сайта 24stanki.ru

// Глобальные переменные
let currentSlide = 0;
let slideInterval;
let isPlaying = true;
let isUserInteracting = false;

// DOM элементы
const carousel = document.querySelector('.carousel');
const slides = document.querySelectorAll('.slide');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const playPauseBtn = document.querySelector('.play-pause-btn');
const nav = document.querySelector('nav');
const dropdowns = document.querySelectorAll('.dropdown');
const faqItems = document.querySelectorAll('.faq-item');

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', () => {
    initCarousel();
    initNavigation();
    initFAQ();
    initScrollAnimation();
    initContactForm();
});

// Карусель
function initCarousel() {
    if (!carousel || !slides.length) return;

    // Инициализация слайдов
    slides.forEach((slide, index) => {
        slide.style.left = `${index * 100}%`;
    });

    // Автоматическая смена слайдов
    startCarousel();

    // Обработчики кнопок
    if (prevBtn) prevBtn.addEventListener('click', () => changeSlide(-1));
    if (nextBtn) nextBtn.addEventListener('click', () => changeSlide(1));
    if (playPauseBtn) {
        playPauseBtn.addEventListener('click', togglePlayPause);
        playPauseBtn.addEventListener('mouseenter', () => isUserInteracting = true);
        playPauseBtn.addEventListener('mouseleave', () => isUserInteracting = false);
    }

    // Автоматическая остановка при наведении
    carousel.addEventListener('mouseenter', () => {
        if (!isUserInteracting) stopCarousel();
    });
    
    carousel.addEventListener('mouseleave', () => {
        if (!isUserInteracting) startCarousel();
    });
}

function changeSlide(direction) {
    currentSlide += direction;
    if (currentSlide < 0) currentSlide = slides.length - 1;
    if (currentSlide >= slides.length) currentSlide = 0;
    
    updateCarousel();
}

function updateCarousel() {
    slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === currentSlide);
    });
}

function startCarousel() {
    if (slideInterval) return;
    slideInterval = setInterval(() => {
        if (!isUserInteracting) {
            changeSlide(1);
        }
    }, 5000);
}

function stopCarousel() {
    clearInterval(slideInterval);
    slideInterval = null;
}

function togglePlayPause() {
    if (isPlaying) {
        stopCarousel();
        playPauseBtn.innerHTML = '▶️';
        playPauseBtn.title = 'Возобновить';
    } else {
        startCarousel();
        playPauseBtn.innerHTML = '⏸️';
        playPauseBtn.title = 'Пауза';
    }
    isPlaying = !isPlaying;
}

// Навигация
function initNavigation() {
    // Фиксация навигации при прокрутке
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });

    // Закрытие выпадающих меню при клике вне
    document.addEventListener('click', (e) => {
        dropdowns.forEach(dropdown => {
            const dropdownContent = dropdown.querySelector('.dropdown-content');
            if (!dropdown.contains(e.target) && dropdownContent) {
                dropdownContent.style.display = 'none';
            }
        });
    });
}

// FAQ
function initFAQ() {
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        const icon = item.querySelector('.faq-icon');

        if (question && answer) {
            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                
                // Закрываем все другие элементы
                faqItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                        const otherAnswer = otherItem.querySelector('.faq-answer');
                        const otherIcon = otherItem.querySelector('.faq-icon');
                        if (otherAnswer) otherAnswer.style.maxHeight = '0px';
                        if (otherIcon) otherIcon.style.transform = 'rotate(0deg)';
                    }
                });

                // Переключаем текущий элемент
                item.classList.toggle('active', !isActive);
                if (!isActive) {
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                    if (icon) icon.style.transform = 'rotate(45deg)';
                } else {
                    answer.style.maxHeight = '0px';
                    if (icon) icon.style.transform = 'rotate(0deg)';
                }
            });
        }
    });
}

// Анимация при прокрутке
function initScrollAnimation() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Наблюдаем за элементами с анимацией
    document.querySelectorAll('section, .review, .stat-item, .feature-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Форма обратной связи
function initContactForm() {
    const form = document.querySelector('.newsletter-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = form.querySelector('input[type="email"]').value;
            
            if (validateEmail(email)) {
                // Здесь можно добавить отправку формы
                alert('Спасибо! Мы свяжемся с вами.');
                form.reset();
            } else {
                alert('Пожалуйста, введите корректный email адрес.');
            }
        });
    }
}

// Валидация email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

// Мобильное меню (если понадобится)
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navUl = document.querySelector('nav ul');
    
    if (menuToggle && navUl) {
        menuToggle.addEventListener('click', () => {
            navUl.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });
    }
}

// Экспорт функций для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initCarousel,
        initNavigation,
        initFAQ,
        initScrollAnimation,
        initContactForm
    };
}
