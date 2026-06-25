document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('filter-sidebar');
    if (!sidebar) return;

    const toggleButton = document.getElementById('toggle-filter-btn');
    const mainContent = document.getElementById('main-content');
    const filterForm = document.getElementById('filter-form');
    const tableBody = document.getElementById('cashflow-table-body');

    const typeSelect = document.querySelector('#filter-form #id_type');
    const categorySelect = document.querySelector('#filter-form #id_category');
    const subcategorySelect = document.querySelector('#filter-form #id_subcategory');

    // --- Логика боковой панели ---
    if (toggleButton) {
        toggleButton.addEventListener('click', () => sidebar.classList.toggle('sidebar-hidden'));
    }

    // --- Логика "живой" фильтрации ---
    let filterTimeout;
    filterForm.addEventListener('input', function(e) {
        clearTimeout(filterTimeout);
        filterTimeout = setTimeout(() => {
            const formData = new FormData(filterForm);
            const params = new URLSearchParams(formData);

            fetch(`?${params.toString()}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                tableBody.innerHTML = html;
                // Повторно инициализируем подсказки для новых кнопок
                $('[data-toggle="tooltip"]').tooltip();
            })
            .catch(error => console.error('Ошибка при обновлении таблицы:', error));
        }, 300); // Небольшая задержка для комфортного ввода
    });

    // --- Логика каскадных списков ---
    function updateSelect(select, options, placeholder) {
        select.innerHTML = `<option value="">${placeholder}</option>`;
        options.forEach(opt => {
            const option = new Option(opt.name, opt.id);
            select.add(option);
        });
    }

    typeSelect.addEventListener('change', function() {
        const typeId = this.value;
        updateSelect(categorySelect, [], "Все категории");
        updateSelect(subcategorySelect, [], "Все подкатегории");
        if (typeId) {
            fetch(`/api/categories/?type_id=${typeId}`)
                .then(response => response.json())
                .then(data => updateSelect(categorySelect, data, "Выберите категорию"));
        }
    });

    categorySelect.addEventListener('change', function() {
        const categoryId = this.value;
        updateSelect(subcategorySelect, [], "Все подкатегории");
        if (categoryId) {
            fetch(`/api/subcategories/?category_id=${categoryId}`)
                .then(response => response.json())
                .then(data => updateSelect(subcategorySelect, data, "Выберите подкатегорию"));
        }
    });

    // Инициализация всплывающих подсказок Bootstrap
    $('[data-toggle="tooltip"]').tooltip();
});
