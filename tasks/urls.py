from django.urls import path
from tasks import views

app_name = "tasks"
urlpatterns = [
    path("", views.tasks, name="tasks"),
    path("category/", views.categories, name="categories"),
    path("update/<int:task_id>/", views.update_task, name="update_task"),
    path("add/", views.add_task, name="add_task"),
    path("del/<int:task_id>/", views.del_task, name="del_task"),
    path(
        "category/update/<int:category_id>/",
        views.update_category,
        name="update_category",
    ),
    path("category/del/<int:category_id>/", views.del_category, name="del_category"),
    path(
        "activate/expired/email/",
        views.activate_expired_email,
        name="activate_expired_email",
    ),
    path(
        "disable/expired/email/",
        views.disable_expired_email,
        name="disable_expired_email",
    ),
    path(
        "activate/deadline/email/",
        views.activate_deadline_email,
        name="activate_deadline_email",
    ),
    path(
        "disable/deadline/email/",
        views.disable_deadline_email,
        name="disable_deadline_email",
    ),
]
