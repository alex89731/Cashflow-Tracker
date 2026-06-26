import django_filters
from django import forms
from .models import CashFlow, Status, Type, Category, Subcategory

class CashFlowFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='created_date', lookup_expr='gte', label='Дата с',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = django_filters.DateFilter(
        field_name='created_date', lookup_expr='lte', label='Дата по',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    type = django_filters.ModelChoiceFilter(
        queryset=Type.objects.all(), label='Тип',
        widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Все типы"
    )
    
    # Изначально набор вариантов пуст. Он будет заполнен в __init__ или через JavaScript.
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.none(), label='Категория',
        widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Все категории"
    )
    
    # Изначально набор вариантов пуст.
    subcategory = django_filters.ModelChoiceFilter(
        queryset=Subcategory.objects.none(), label='Подкатегория',
        widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Все подкатегории"
    )

    class Meta:
        model = CashFlow
        fields = ['start_date', 'end_date', 'status', 'type', 'category', 'subcategory']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Эта логика выполняется на сервере ПЕРЕД отправкой страницы в браузер.
        # Она гарантирует, что если фильтр уже был применен (например, после перезагрузки страницы),
        # в выпадающих списках будут правильные, уже отфильтрованные опции.
        
        selected_type = self.data.get('type')
        if selected_type:
            self.form.fields['category'].queryset = Category.objects.filter(type_id=selected_type)
        
        selected_category = self.data.get('category')
        if selected_category:
            self.form.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=selected_category)
