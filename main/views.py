import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import EducationForm, ProjectForm, SkillsForm
from main.models import Education, Experience, Project, Skills

PORTFOLIO_OWNER_NAME = "Rafif Ananta Marpaung"


def show_main(request):
    last_login = request.COOKIES.get("last_login", "Belum ada sesi login / Cookie tidak ditemukan")
    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "npm": "2506585151",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "IT Enthusiast, Third semester, Studying at Fasilkom UI"
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # JSON dibangun manual supaya bisa menyertakan status star milik user yang sedang login
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "link": project.link,
                "thumbnail": project.thumbnail,
                "star_count": len(starred_users),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            },
        })

    return JsonResponse(data, safe=False)


def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

@login_required(login_url="/login/")
def create_project(request):
    # Hanya pemilik portofolio (superuser) yang boleh menambah proyek
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
    }
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")
    return redirect("main:show_projects")


# Tanpa cek is_superuser: semua akun yang login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")


# ---------- Education section ----------

def get_education_json(request):
    education_entries = Education.objects.all()
    education_json = serializers.serialize("json", education_entries)
    return HttpResponse(education_json, content_type="application/json")


def show_education(request):
    json_response = get_education_json(request)
    education_entries = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [entry.object for entry in education_entries]

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "education_list": education_list,
    }
    return render(request, "education.html", context)


def create_education(request):
    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
        "is_edit": False,
    }
    return render(request, "education_form.html", context)


def update_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
        "is_edit": True,
        "education": education,
    }
    return render(request, "education_form.html", context)


def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")
    return redirect("main:show_education")

#------- Skills Section --------------

def get_skills_json(request):
    skills_entries = Skills.objects.all()
    skills_json = serializers.serialize("json", skills_entries)
    return HttpResponse(skills_json, content_type="application/json")


def show_skills(request):
    json_response = get_skills_json(request)
    skills_entries = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills_list = [entry.object for entry in skills_entries]

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "skills_list": skills_list,
    }
    return render(request, "skills.html", context)

def create_skills(request):
    form = SkillsForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill berhasil ditambahkan!")
        return redirect("main:show_skills")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
        "is_edit": False,
    }
    return render(request, "skills_form.html", context)

def delete_skills(request, skills_id):
    skill = get_object_or_404(Skills, id=skills_id)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus.")
        return redirect('main:show_skills')
    return redirect('main:show_skills')


# ---------- Authentication ----------

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response
