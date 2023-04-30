from django.forms import *


class UserSort(forms.Form):
    FRAMEWORKS_CHOICES = [
        ('uploaded', 'Сначала новые'),
        ('-uploaded', 'Сначала старые'),
        ('name', 'По алфавиту А-Я'),
        ('-name', 'По алфавиту Я-А'),
        ('-price', 'От дорогих к дешевым'),
        ('price', 'От дешевых к дорогим')
    ]

    frameworks = ChoiceField(
        label='',
        choices=FRAMEWORKS_CHOICES,
        widget=Select(attrs={'size': 1, 'class': 'sorting-items', 'name': 'category'}),
    )
