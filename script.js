document.addEventListener('DOMContentLoaded', function() {
    // Эффект навигации при скролле
    const nav = document.querySelector('nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });

    // Плавная прокрутка для навигационных ссылок
    document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Инициализация карусели
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    let currentSlide = 0;
    let slideInterval;

    // Показываем первый слайд
    slides[currentSlide].classList.add('active');

    // Функция для переключения слайда с анимацией
    function goToSlide(n) {
        slides[currentSlide].style.opacity = '0';
        slides[currentSlide].style.transform = 'scale(0.95)';
        
        setTimeout(() => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (n + totalSlides) % totalSlides;
            slides[currentSlide].classList.add('active');
            
            setTimeout(() => {
                slides[currentSlide].style.opacity = '1';
                slides[currentSlide].style.transform = 'scale(1)';
            }, 50);
        }, 300);
    }

    // Автоматическое переключение
    function startSlideShow() {
        slideInterval = setInterval(() => {
            goToSlide(currentSlide + 1);
        }, 5000);
    }

    // Остановка автоматического переключения
    function pauseSlideShow() {
        clearInterval(slideInterval);
    }

    // Пауза при наведении
    const carousel = document.querySelector('.carousel');
    if (carousel) {
        carousel.addEventListener('mouseenter', pauseSlideShow);
        carousel.addEventListener('mouseleave', startSlideShow);
    }

    // Обработка касаний для мобильных устройств
    let touchStartX = 0;
    let touchEndX = 0;

    carousel.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
        pauseSlideShow();
    }, false);

    carousel.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
        startSlideShow();
    }, false);

    function handleSwipe() {
        if (touchEndX < touchStartX - 50) {
            goToSlide(currentSlide + 1); // Свайп влево
        }
        if (touchEndX > touchStartX + 50) {
            goToSlide(currentSlide - 1); // Свайп вправо
        }
    }

    // Запускаем карусель
    startSlideShow();

    // Инициализация первого слайда как активного
    if (slides.length > 0) {
        slides[0].classList.add('active');
        slides[0].style.opacity = '1';
        slides[0].style.transform = 'scale(1)';
    }

    // Анимация появления элементов при скролле
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

    // Применяем анимацию ко всем секциям
    document.querySelectorAll('section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(section);
    });

    // Анимация для отзывов
    document.querySelectorAll('.review').forEach((review, index) => {
        review.style.opacity = '0';
        review.style.transform = 'translateY(30px)';
        review.style.transition = `opacity 0.6s ease-out ${index * 0.1}s, transform 0.6s ease-out ${index * 0.1}s`;
        observer.observe(review);
    });

    // Эффект параллакса для плавающих элементов
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallax = document.querySelector('.floating-elements');
        if (parallax) {
            parallax.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });

    // Анимация для навигационных ссылок
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Анимация для кнопок
    document.querySelectorAll('button, .whatsapp, .telegram').forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
        });
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Плавная загрузка изображений
    const images = document.querySelectorAll('img');
    const imageOptions = {
        threshold: 0,
        rootMargin: '0px 0px 50px 0px'
    };

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.style.opacity = '0';
                img.style.transition = 'opacity 0.5s ease-in-out';
                
                img.addEventListener('load', () => {
                    img.style.opacity = '1';
                });
                
                observer.unobserve(img);
            }
        });
    }, imageOptions);

    images.forEach(img => imageObserver.observe(img));

    // FAQ функциональность
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            // Закрываем все остальные элементы
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                }
            });
            
            // Переключаем текущий элемент
            item.classList.toggle('active');
        });
    });
});
