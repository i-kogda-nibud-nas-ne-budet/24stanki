// Хлебные крошки (Breadcrumbs) для 24stanki.ru
// Автоматически генерирует навигационную цепочку на основе текущей страницы

document.addEventListener('DOMContentLoaded', function() {
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
        'sravnenie-listogibov-i-gilotin.html': 'Листогибы vs Гильотины',
        'sravnenie-trubogibov-i-profilgebiv.html': 'Трубогибы vs Профилегибы',
        'kakoj-stanok-vybrat-dlya-proizvodstva.html': 'Выбор станка',
        'top-10-luchshih-markov-stankov-2025.html': 'Топ-10 марок 2025',
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

    // Определяем родительские страницы
    function getParentPage(page) {
        if (page.startsWith('remont-') && !page.includes('blog')) {
            return { name: 'Услуги', url: 'uslugi.html' };
        } else if (page.startsWith('blog-')) {
            return { name: 'Блог', url: 'blog.html' };
        } else if (page.startsWith('sravnenie-') || page.startsWith('kakoj-') || page.startsWith('top-10-')) {
            return { name: 'Блог', url: 'blog.html' };
        }
        return null;
    }

    // Создаём HTML хлебных крошек
    let breadcrumbHTML = '<ol itemscope itemtype="https://schema.org/BreadcrumbList">';
    let position = 1;
    
    // Главная всегда первая
    breadcrumbHTML += `
        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <a itemprop="item" href="index.html"><span itemprop="name">Главная</span></a>
            <meta itemprop="position" content="${position}" />
        </li>
    `;
    
    const pageName = pageNames[currentPage] || currentPage;
    const parentPage = getParentPage(currentPage);

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
});
