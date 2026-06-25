from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from cashflow.models import Status, Type, Category, Subcategory, CashFlow
import random
from decimal import Decimal
from datetime import timedelta

class Command(BaseCommand):
    help = 'Заполняет базу данных исчерпывающими тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начинаем очистку старых данных...')
        # Удаляем только то, что создаем, не трогая суперпользователей
        User.objects.filter(is_superuser=False).delete()
        CashFlow.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        Type.objects.all().delete()
        Status.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Старые данные очищены.'))

        # --- Создание пользователей ---
        self.stdout.write('Создаем пользователей...')
        User.objects.create_user('testuser1', 'test1@example.com', 'password123')
        User.objects.create_user('testuser2', 'test2@example.com', 'password123')
        self.stdout.write(self.style.SUCCESS('Пользователи созданы.'))

        # --- Создание справочников ---
        self.stdout.write('Создаем справочники...')
        status_biz = Status.objects.create(name='Бизнес')
        status_pers = Status.objects.create(name='Личное')
        status_tax = Status.objects.create(name='Налог')

        type_income = Type.objects.create(name='Пополнение')
        type_expense = Type.objects.create(name='Списание')

        # Категории и подкатегории для Списания
        cat_infra = Category.objects.create(name='Инфраструктура', type=type_expense)
        Subcategory.objects.create(name='VPS/VDS Серверы', category=cat_infra)
        Subcategory.objects.create(name='Прокси', category=cat_infra)
        Subcategory.objects.create(name='Домены', category=cat_infra)

        cat_marketing = Category.objects.create(name='Маркетинг', type=type_expense)
        Subcategory.objects.create(name='Farpost', category=cat_marketing)
        Subcategory.objects.create(name='Avito', category=cat_marketing)

        cat_transport = Category.objects.create(name='Транспорт', type=type_expense)
        Subcategory.objects.create(name='Такси', category=cat_transport)
        Subcategory.objects.create(name='Бензин', category=cat_transport)

        # Категории и подкатегории для Пополнения
        cat_salary = Category.objects.create(name='Зарплата', type=type_income)
        Subcategory.objects.create(name='Аванс', category=cat_salary)
        Subcategory.objects.create(name='Основная часть', category=cat_salary)

        cat_freelance = Category.objects.create(name='Фриланс', type=type_income)
        Subcategory.objects.create(name='Проект "Веб-сервис"', category=cat_freelance)
        Subcategory.objects.create(name='Консультации', category=cat_freelance)
        
        self.stdout.write(self.style.SUCCESS('Справочники созданы.'))

        # --- Создание тестовых записей для КАЖДОЙ категории ---
        self.stdout.write('Создаем тестовые записи о ДДС для всех категорий...')
        all_categories = Category.objects.all()
        statuses = [status_biz, status_pers, status_tax]
        record_count = 0

        for category in all_categories:
            subcategories = list(category.subcategories.all())
            if not subcategories:
                continue  # Пропускаем категории без подкатегорий

            # Создаем по 2-3 записи на каждую категорию
            for _ in range(random.randint(2, 3)):
                subcategory = random.choice(subcategories)
                CashFlow.objects.create(
                    created_date=timezone.now() - timedelta(days=random.randint(0, 90)),
                    status=random.choice(statuses),
                    type=category.type,  # Тип берется от родительской категории
                    category=category,
                    subcategory=subcategory,
                    amount=Decimal(random.randrange(1000, 50000)) / 100,
                    comment=f'Автоматическая запись #{record_count + 1}'
                )
                record_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'{record_count} тестовых записей создано.'))
        self.stdout.write(self.style.SUCCESS('Миграция данных успешно завершена!'))
