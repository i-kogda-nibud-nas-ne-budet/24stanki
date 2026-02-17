document.addEventListener('DOMContentLoaded', function() {
    // Управление видео
    const video = document.querySelector('.hero-video');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const controlIcon = playPauseBtn ? playPauseBtn.querySelector('.control-icon') : null;
    
    if (video && playPauseBtn && controlIcon) {
        playPauseBtn.addEventListener('click', function() {
            if (video.muted) {
                video.muted = false;
                controlIcon.textContent = '🔊';
            } else {
                video.muted = true;
                controlIcon.textContent = '🔇';
            }
        });
    }

    // Гамбургер-меню
    const hamburger = document.querySelector('.hamburger');
    const navUl = document.querySelector('nav ul');
    const dropdowns = document.querySelectorAll('.dropdown');
    
    if (hamburger && navUl) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navUl.classList.toggle('active');
            
            // Обновляем aria-expanded для доступности
            const isExpanded = hamburger.classList.contains('active');
            hamburger.setAttribute('aria-expanded', isExpanded);
        });
        
        // Закрытие меню при клике на ссылку
        navUl.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    hamburger.classList.remove('active');
                    navUl.classList.remove('active');
                    hamburger.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }
    
    // Dropdown на мобильных
    dropdowns.forEach(dropdown => {
        const dropbtn = dropdown.querySelector('.dropbtn');
        if (dropdown && window.innerWidth <= 768) {
            dropbtn.addEventListener('click', function(e) {
                e.preventDefault();
                dropdown.classList.toggle('active');
            });
        }
    });

    // Эффект навигации при скролле
    const nav = document.querySelector('nav');
    if (nav) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });
    }

    // Плавная прокрутка для навигационных ссылок
    document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId !== '#' && targetId.startsWith('#')) {
                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    // Учитываем высоту навигации
                    const navHeight = nav ? nav.offsetHeight : 0;
                    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Карусель
    const carousel = document.querySelector('.carousel');
    if (carousel) {
        const slides = carousel.querySelectorAll('.slide');
        let currentSlide = 0;

        // Функция для показа слайда
        function showSlide(index) {
            // Убираем класс active у всех слайдов
            slides.forEach(slide => slide.classList.remove('active'));
            
            // Добавляем класс active к нужному слайду
            if (slides[index]) {
                slides[index].classList.add('active');
            }
        }

        // Показываем первый слайд
        if (slides.length > 0) {
            showSlide(currentSlide);
        }

        // Автоматическая смена слайдов каждые 5 секунд
        setInterval(() => {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        }, 5000);
    }

    // FAQ функциональность
    const faqContainers = document.querySelectorAll('.faq-container');
    
    faqContainers.forEach(container => {
        const faqItems = container.querySelectorAll('.faq-item');
        
        faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            const icon = question ? question.querySelector('.faq-icon') : null;
            
            // Убедимся, что все FAQ изначально свернуты
            item.classList.remove('active');
            if (icon) {
                icon.textContent = '+';
            }
            
            if (question) {
                question.addEventListener('click', () => {
                    // Закрываем все остальные элементы в том же контейнере
                    faqItems.forEach(otherItem => {
                        if (otherItem !== item && otherItem.classList.contains('active')) {
                            otherItem.classList.remove('active');
                            const otherIcon = otherItem.querySelector('.faq-icon');
                            if (otherIcon) {
                                otherIcon.textContent = '+';
                            }
                        }
                    });
                    
                    // Переключаем текущий элемент
                    item.classList.toggle('active');
                    if (icon) {
                        icon.textContent = item.classList.contains('active') ? '−' : '+';
                    }
                });
            }
        });
    });
});
