from django.shortcuts import render, redirect, get_object_or_404
from .models import CashFlow, Category, Subcategory
from .forms import CashFlowForm
from .filters import CashFlowFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategorySerializer, SubcategorySerializer

def cashflow_list(request):
    """
    Представление для отображения списка записей о ДДС.
    Применяет фильтр на основе GET-параметров запроса.
    Если запрос является AJAX-запросом, возвращает только фрагмент таблицы.
    """
    cashflow_filter = CashFlowFilter(request.GET, queryset=CashFlow.objects.select_related('status', 'type', 'category', 'subcategory').all())
    
    # Проверяем, является ли запрос AJAX-запросом
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'cashflow/partials/table_body.html', {'filter': cashflow_filter})

    return render(request, 'cashflow/cashflow_list.html', {'filter': cashflow_filter})

def cashflow_create(request):
    """
    Представление для создания новой записи о ДДС.
    """
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cashflow_list')
    else:
        form = CashFlowForm()
    return render(request, 'cashflow/cashflow_form.html', {'form': form})

def cashflow_update(request, pk):
    """
    Представление для редактирования существующей записи.
    """
    cashflow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=cashflow)
        if form.is_valid():
            form.save()
            return redirect('cashflow_list')
    else:
        form = CashFlowForm(instance=cashflow)
    return render(request, 'cashflow/cashflow_form.html', {'form': form, 'cashflow': cashflow})

def cashflow_delete(request, pk):
    """
    Представление для удаления записи.
    """
    cashflow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        cashflow.delete()
        return redirect('cashflow_list')
    return render(request, 'cashflow/cashflow_confirm_delete.html', {'cashflow': cashflow})


class CategoryAPIView(APIView):
    """
    API для получения категорий, связанных с определенным типом.
    """
    def get(self, request):
        type_id = request.query_params.get('type_id')
        if not type_id:
            return Response([])
        try:
            categories = Category.objects.filter(type_id=type_id)
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        except (ValueError, TypeError):
            return Response([])

class SubcategoryAPIView(APIView):
    """
    API для получения подкатегорий, связанных с определенной категорией.
    """
    def get(self, request):
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response([])
        try:
            subcategories = Subcategory.objects.filter(category_id=category_id)
            serializer = SubcategorySerializer(subcategories, many=True)
            return Response(serializer.data)
        except (ValueError, TypeError):
            return Response([])
