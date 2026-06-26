document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('filter-sidebar');
    if (!sidebar) return; // Если боковой панели нет на странице, ничего не делаем.

    const toggleButton = document.getElementById('toggle-filter-btn');
    const mainContent = document.getElementById('main-content');
    const filterForm = document.getElementById('filter-form');
    const tableBody = document.getElementById('cashflow-table-body');

    const typeSelect = document.querySelector('#filter-form #id_type');
    const categorySelect = document.querySelector('#filter-form #id_category');
    const subcategorySelect = document.querySelector('#filter-form #id_subcategory');

    // --- Логика для скрытия/показа боковой панели ---
    if (toggleButton) {
        toggleButton.addEventListener('click', () => sidebar.classList.toggle('sidebar-hidden'));
    }

    // --- Логика "живой" фильтрации (без перезагрузки страницы) ---
    let filterTimeout; // Переменная для хранения таймера
    filterForm.addEventListener('input', function(e) {
        // Очищаем предыдущий таймер, если он был
        clearTimeout(filterTimeout);
        // Устанавливаем новый таймер. Функция выполнится через 300 мс после последнего изменения.
        filterTimeout = setTimeout(() => {
            const formData = new FormData(filterForm);
            const params = new URLSearchParams(formData);

            // Отправляем AJAX-запрос на тот же URL, но с параметрами фильтра
            fetch(`?${params.toString()}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Этот заголовок помогает Django понять, что это AJAX
                }
            })
            .then(response => response.text()) // Получаем ответ как HTML-текст
            .then(html => {
                tableBody.innerHTML = html; // Заменяем содержимое таблицы на новое
                // После обновления таблицы нужно заново инициализировать всплывающие подсказки Bootstrap
                $('[data-toggle="tooltip"]').tooltip();
            })
            .catch(error => console.error('Ошибка при обновлении таблицы:', error));
        }, 300); // Задержка в 300 мс, чтобы не отправлять запрос на каждое нажатие клавиши.
    });

    // --- Логика для каскадных (зависимых) выпадающих списков ---
    function updateSelect(select, options, placeholder) {
        select.innerHTML = `<option value="">${placeholder}</option>`; // Очищаем список и добавляем "пустой" вариант
        options.forEach(opt => {
            const option = new Option(opt.name, opt.id);
            select.add(option);
        });
    }

    // При изменении "Типа"
    typeSelect.addEventListener('change', function() {
        const typeId = this.value;
        // Очищаем списки Категорий и Подкатегорий
        updateSelect(categorySelect, [], "Все категории");
        updateSelect(subcategorySelect, [], "Все подкатегории");
        // Если тип выбран, запрашиваем для него категории
        if (typeId) {
            fetch(`/api/categories/?type_id=${typeId}`)
                .then(response => response.json())
                .then(data => updateSelect(categorySelect, data, "Выберите категорию"));
        }
    });

    // При изменении "Категории"
    categorySelect.addEventListener('change', function() {
        const categoryId = this.value;
        // Очищаем список Подкатегорий
        updateSelect(subcategorySelect, [], "Все подкатегории");
        // Если категория выбрана, запрашиваем для нее подкатегории
        if (categoryId) {
            fetch(`/api/subcategories/?category_id=${categoryId}`)
                .then(response => response.json())
                .then(data => updateSelect(subcategorySelect, data, "Выберите подкатегорию"));
        }
    });

    // Инициализируем всплывающие подсказки Bootstrap при первой загрузке страницы
    $('[data-toggle="tooltip"]').tooltip();
});
