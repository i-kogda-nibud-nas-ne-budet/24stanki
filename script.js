document.addEventListener('DOMContentLoaded', function() {
    // ===== ХЛЕБНЫЕ КРОШКИ (BREADCRUMBS) =====
    function generateBreadcrumbs() {
        const breadcrumbsContainer = document.querySelector('.breadcrumbs');
        if (!breadcrumbsContainer) return;

        const currentUrl = window.location.pathname;
        const currentPage = currentUrl.split('/').pop() || 'index.html';
        
        // Отображаемые названия для страниц
        const pageNames = {
            'index.html': 'Главная',
            'uslugi.html': 'Услуги',
            'blog.html': 'Блог',
            'remont-listogibov.html': 'Ремонт листогибов',
            'remont-gilotin.html': 'Ремонт гильотин',
            'remont-lentochnyh-pil.html': 'Ремонт ленточных пил',
            'remont-profilgebiv.html': 'Ремонт профилегибов',
            'remont-valtsev.html': 'Ремонт вальцевых станков',
            'remont-trubogibov.html': 'Ремонт трубогибов',
            'remont-stankov-chpu.html': 'Ремонт станков ЧПУ',
            'sravnenie-listogibov-i-gilotin.html': 'Сравнение: листогибы vs гильотины',
            'sravnenie-trubogibov-i-profilgebiv.html': 'Сравнение: трубогибы vs профилегибы',
            'kakoj-stanok-vybrat-dlya-proizvodstva.html': 'Как выбрать станок для производства',
            'top-10-luchshih-markov-stankov-2025.html': 'Топ-10 марок станков 2025',
            'blog-obsluzhivanie-listogibov.html': 'Обслуживание листогибов',
            'blog-remont-listogibov-chpu.html': 'Ремонт листогибов ЧПУ',
            'blog-remont-trubogibov.html': 'Ремонт трубогибов',
            'blog-remont-lentochnyh-pil.html': 'Ремонт ленточных пил',
            'blog-remont-gilotin.html': 'Ремонт гильотин',
            'blog-zapchasti-listogibov.html': 'Запчасти для листогибов',
            'blog-kapitalnyi-remont-pressa.html': 'Капитальный ремонт пресса',
            'blog-remont-profilgebiv.html': 'Ремонт профилегибов',
            'blog-remont-valtsev.html': 'Ремонт вальцевых станков',
            'blog-remont-cpu-stoiki.html': 'Ремонт ЧПУ стойки',
            'blog-remont-listogiba.html': 'Признаки поломки листогиба',
            'remont-listogibov-moskva.html': 'Ремонт листогибов в Москве',
            'remont-gilotin-moskva.html': 'Ремонт гильотин в Москве',
            'remont-trubogibov-moskva.html': 'Ремонт трубогибов в Москве',
            'remont-listogibov-spb.html': 'Ремонт листогибов в Санкт-Петербурге',
            'remont-gilotin-spb.html': 'Ремонт гильотин в Санкт-Петербурге',
            'remont-trubogibov-spb.html': 'Ремонт трубогибов в Санкт-Петербурге',
            'remont-listogibov-ekaterinburg.html': 'Ремонт листогибов в Екатеринбурге',
            'remont-gilotin-ekaterinburg.html': 'Ремонт гильотин в Екатеринбурге',
            'remont-trubogibov-ekaterinburg.html': 'Ремонт трубогибов в Екатеринбурге',
            'remont-listogibov-novosibirsk.html': 'Ремонт листогибов в Новосибирске',
            'remont-gilotin-novosibirsk.html': 'Ремонт гильотин в Новосибирске',
            'remont-trubogibov-novosibirsk.html': 'Ремонт трубогибов в Новосибирске'
        };

        // Определяем структуру страниц
        const pathStructure = {
            'remont': { name: 'Услуги', url: 'uslugi.html' },
            'blog': { name: 'Блог', url: 'blog.html' },
            'sravnenie': { name: 'Статьи', url: 'blog.html' }
        };

        // Создаём HTML хлебных крошек
        let breadcrumbHTML = '<ol itemscope itemtype="https://schema.org/BreadcrumbList">';
        
        // Главная всегда первая
        let position = 1;
        breadcrumbHTML += `
            <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                <a itemprop="item" href="index.html"><span itemprop="name">Главная</span></a>
                <meta itemprop="position" content="${position}" />
            </li>
        `;
        
        // Определяем родительскую страницу
        let parentPage = null;
        const pageName = pageNames[currentPage] || currentPage;
        
        if (currentPage.startsWith('remont-') && !currentPage.includes('blog')) {
            parentPage = { name: 'Услуги', url: 'uslugi.html' };
        } else if (currentPage.startsWith('blog-')) {
            parentPage = { name: 'Блог', url: 'blog.html' };
        } else if (currentPage.startsWith('sravnenie-') || currentPage.startsWith('kakoj-') || currentPage.startsWith('top-10-')) {
            parentPage = { name: 'Блог', url: 'blog.html' };
        }

        // Добавляем родительскую страницу
        if (parentPage && currentPage !== 'uslugi.html' && currentPage !== 'blog.html') {
            position++;
            breadcrumbHTML += `
                <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                    <a itemprop="item" href="${parentPage.url}"><span itemprop="name">${parentPage.name}</span></a>
                    <meta itemprop="position" content="${position}" />
                </li>
            `;
        }

        // Текущая страница
        if (currentPage !== 'index.html') {
            position++;
            breadcrumbHTML += `
                <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                    <span itemprop="name" aria-current="page">${pageName}</span>
                    <meta itemprop="position" content="${position}" />
                </li>
            `;
        }

        breadcrumbHTML += '</ol>';
        breadcrumbsContainer.innerHTML = breadcrumbHTML;
    }

    // Запускаем генерацию хлебных крошек
    generateBreadcrumbs();

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
