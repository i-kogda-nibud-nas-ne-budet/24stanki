// Функционал для страницы блога

document.addEventListener('DOMContentLoaded', function() {
    // Фильтрация статей по категориям
    const filterButtons = document.querySelectorAll('.filter-btn');
    const blogCards = document.querySelectorAll('.blog-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Удаляем активный класс у всех кнопок
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Добавляем активный класс нажатой кнопке
            this.classList.add('active');
            
            const category = this.getAttribute('data-category');
            
            // Фильтрация статей
            blogCards.forEach(card => {
                if (category === 'all' || card.getAttribute('data-category') === category) {
                    card.style.display = 'block';
                    // Добавляем анимацию появления
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 100);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
    
    // Загрузка большего количества статей
    const loadMoreBtn = document.querySelector('.load-more-btn');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            // Здесь можно добавить логику загрузки дополнительных статей
            // Например, через AJAX или показ скрытых элементов
            
            // Временно выводим сообщение о загрузке
            this.textContent = 'Загрузка...';
            this.disabled = true;
            
            setTimeout(() => {
                this.textContent = 'Загрузить больше статей';
                this.disabled = false;
                // Показываем сообщение о новых статьях
                showNotification('Новые статьи скоро появятся!');
            }, 2000);
        });
    }
    
    // Анимация появления карточек при загрузке страницы
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Применяем анимацию ко всем карточкам
    blogCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `opacity 0.5s ease ${index * 0.1}s, transform 0.5s ease ${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Функция показа уведомлений
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        
        // Стили уведомления
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 15px 25px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        // Добавляем анимацию
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(notification);
        
        // Убираем уведомление через 3 секунды
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // Поиск по статьям
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = 'Поиск по статьям...';
    searchInput.className = 'blog-search';
    
    // Добавляем стили для поиска
    const searchStyle = document.createElement('style');
    searchStyle.textContent = `
        .blog-search {
            width: 100%;
            padding: 12px 20px;
            margin: 20px 0;
            border: 2px solid #333;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .blog-search:focus {
            outline: none;
            border-color: #4CAF50;
            background: rgba(255, 255, 255, 0.2);
        }
        
        .blog-search::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
    `;
    document.head.appendChild(searchStyle);
    
    // Вставляем поиск перед фильтрами
    const blogFilters = document.querySelector('.blog-filters');
    if (blogFilters) {
        blogFilters.insertBefore(searchInput, blogFilters.firstChild);
    }
    
    // Функция поиска
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        blogCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const content = card.querySelector('p').textContent.toLowerCase();
            
            if (title.includes(searchTerm) || content.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
    
    // Кнопка "Читать статью" - добавление функционала
    const readMoreButtons = document.querySelectorAll('.read-more');
    readMoreButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Получаем заголовок статьи
            const articleTitle = this.closest('.blog-card').querySelector('h3').textContent;
            
            // Показываем уведомление
            showNotification(`Статья "${articleTitle}" находится в разработке`);
        });
    });
});
