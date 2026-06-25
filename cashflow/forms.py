from django import forms
from .models import CashFlow, Type, Category, Subcategory

class CashFlowForm(forms.ModelForm):
    """
    Форма для создания и редактирования записей о ДДС.
    """
    class Meta:
        model = CashFlow
        fields = ['created_date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'created_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'status': forms.Select(attrs={'required': True}),
            'type': forms.Select(attrs={'required': True}),
            'category': forms.Select(attrs={'required': True}),
            'subcategory': forms.Select(attrs={'required': True}),
            'amount': forms.NumberInput(attrs={'required': True, 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Конструктор формы для реализации каскадных полей.
        """
        super().__init__(*args, **kwargs)
        
        # Изначально списки категорий и подкатегорий пусты
        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        # Если форма отправлена (в self.data есть данные)
        if self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id).order_by('name')
                
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        # Если форма открыта для редактирования существующей записи
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type).order_by('name')
            self.fields['subcategory'].queryset = self.instance.category.subcategories.order_by('name')

    def clean(self):
        """
        Валидация зависимостей между полями.
        """
        cleaned_data = super().clean()
        
        type_ = cleaned_data.get("type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")
        
        if type_ and category and category.type != type_:
            raise forms.ValidationError("Выбранная категория не относится к указанному типу.")
        
        if category and subcategory and subcategory.category != category:
            raise forms.ValidationError("Выбранная подкатегория не относится к указанной категории.")
        
        return cleaned_data
