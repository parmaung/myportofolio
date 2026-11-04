from django.urls import path

from main.views import (
    create_education,
    create_project,
    delete_education,
    delete_project,
    get_education_json,
    get_projects_json,
    show_education,
    show_experience,
    show_main,
    show_projects,
    update_education,
    get_skills_json,
    show_skills,
    create_skills,
    delete_skills,
    register,
    login_user,
    logout_user,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", show_projects, name="show_projects"),
    path("skills/", show_skills, name="show_skills"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path(
        "education/<uuid:education_id>/edit/",
        update_education,
        name="update_education",
    ),
    path(
        "education/<uuid:education_id>/delete/",
        delete_education,
        name="delete_education",
    ),
    path("api/education/", get_education_json, name="get_education_json"),
    path("skills/add/", create_skills, name="create_skills"),
    path("skills/<uuid:skills_id>/delete/", delete_skills, name="delete_skills"),
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]
