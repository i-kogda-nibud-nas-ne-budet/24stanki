document.addEventListener('DOMContentLoaded', function() {
    // Управление видео
    const video = document.querySelector('.hero-video');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const controlIcon = playPauseBtn.querySelector('.control-icon');
    
    if (video && playPauseBtn) {
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
            slides[index].classList.add('active');
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
            const icon = question.querySelector('.faq-icon');
            
            // Убедимся, что все FAQ изначально свернуты
            item.classList.remove('active');
            if (icon) {
                icon.textContent = '+';
            }
            
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
        });
    });
});
