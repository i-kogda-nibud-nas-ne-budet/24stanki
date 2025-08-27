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

    // FAQ функциональность
    const faqContainers = document.querySelectorAll('.faq-container');
    
    faqContainers.forEach(container => {
        const faqItems = container.querySelectorAll('.faq-item');
        
        faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            const icon = question.querySelector('.faq-icon');
            
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
