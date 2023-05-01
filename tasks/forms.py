from django import forms
from django.forms import ModelForm
import django_filters
from tasks.models import Category, Task


class CategoryForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите название"}
        )
    )

    class Meta:
        model = Category
        fields = ("name",)


class SortForm(forms.Form):
    sort_mapping = (
        (
            "-name",
            "По алфавиту",
        ),
        ("-deadline", "По дате выполнения"),
        ("priority", "Приоритет +"),
        ("-priority", "Приоритет -"),
    )
    sort_form = forms.TypedChoiceField(
        label="Сортировка",
        choices=sort_mapping,
        widget=forms.Select(),
        initial="-name",
        required=False,
    )


class TaskFilter(django_filters.FilterSet):
    deadline = django_filters.DateTimeFilter(
        field_name="deadline",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.none())

    def __init__(self, user, *args, **kwargs):
        super(TaskFilter, self).__init__(*args, **kwargs)
        self.filters["category"].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Task
        fields = ["category", "deadline", "priority", "completed"]


class TaskForm(ModelForm):
    attrs = {"class": "form-control"}
    name = forms.CharField(widget=forms.TextInput(attrs=attrs))
    text = forms.CharField(widget=forms.Textarea(attrs=attrs), required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=forms.Select(attrs=attrs),
        required=False,
    )
    completed = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        ),
        required=False,
    )
    priority = forms.IntegerField(widget=forms.TextInput(attrs=attrs), required=False)

    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Task
        exclude = ["user", "timestamp"]
