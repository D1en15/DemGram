from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accounts.models import User
from tasks.models import Task, Category
from tasks.forms import CategoryForm, TaskForm, SortForm
from accounts.forms import DeadlineEmailTimeForm
from tasks.forms import TaskFilter


def homepage(request):
    return render(request, "tasks/homepage.html")


@login_required
def tasks(request):
    sort_form = SortForm(request.POST)
    if sort_form.is_valid() and sort_form.cleaned_data.get("sort_form"):
        needed_sort = sort_form.cleaned_data.get("sort_form")
    else:
        needed_sort = "-name"
    tasks = Task.objects.filter(user=request.user).order_by(needed_sort)
    filter = TaskFilter(request.user, request.GET, queryset=tasks)
    context = {
        "filter": filter,
        "sort": sort_form,
        "user": User.objects.get(id=request.user.id),
    }
    return render(request, "tasks/tasks.html", context)


@login_required
def del_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.user != request.user:
        return redirect(reverse("accounts:login"))
    else:
        task.delete()
        return redirect(request.META["HTTP_REFERER"])


@login_required
def categories(request):
    categories = Category.objects.filter(user=request.user.id)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(request.META["HTTP_REFERER"])
    else:
        form = CategoryForm()
    context = {"categories": categories, "form": form}
    return render(request, "tasks/categories.html", context)


@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(reverse("tasks:tasks"))
    else:
        form = TaskForm(request.user)

    categories = Category.objects.filter(user_id=request.user)
    context = {"form": form, "categories": categories}
    return render(request, "tasks/add_task.html", context)


@login_required
def update_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.user != request.user:
        return redirect(reverse("accounts:login"))
    else:
        if request.method == "POST":
            form = TaskForm(request.user, request.POST, instance=task)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.is_expired_check = False
                post.save()
                return redirect(reverse("tasks:tasks"))
        else:
            form = TaskForm(request.user, instance=task)

        context = {"form": form}
        return render(request, "tasks/update_task.html", context)


@login_required
def update_category(request, category_id):
    post = get_object_or_404(Category, id=category_id, user=request.user)
    if post.user != request.user:
        return redirect(reverse("accounts:login"))
    else:
        if request.method == "POST":
            form = CategoryForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.user_id = request.user
                post.save()
                return redirect(reverse("tasks:categories"))
        else:
            form = CategoryForm(instance=post)
        context = {"category": post, "form": form}
        return render(request, "tasks/categories_update.html", context)


@login_required
def del_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if category.user != request.user:
        return redirect(reverse("accounts:login"))
    else:
        category.delete()
        return redirect(request.META["HTTP_REFERER"])


@login_required
def activate_expired_email(request):
    user = User.objects.get(id=request.user.id)
    user.expired_email = True
    user.save()
    return redirect(request.META["HTTP_REFERER"])


@login_required
def disable_expired_email(request):
    user = User.objects.get(id=request.user.id)
    user.expired_email = False
    user.save()
    return redirect(reverse("homepage"))


@login_required
def activate_deadline_email(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = DeadlineEmailTimeForm(request.POST)
        if form.is_valid():
            user.deadline_email_time = form.cleaned_data["time"]
            user.deadline_email = True
            user.save()
            return redirect(reverse("tasks:tasks"))
    else:
        form = DeadlineEmailTimeForm()
    return render(request, "tasks/set_deadline_time.html", {"form": form})


@login_required
def disable_deadline_email(request):
    user = User.objects.get(id=request.user.id)
    user.deadline_email = False
    user.save()
    return redirect(request.META["HTTP_REFERER"])
