from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import EducationForm, ProjectForm
from main.models import Education, Experience, Project

PORTFOLIO_OWNER_NAME = "Rafif Ananta Marpaung"


def show_main(request):
    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "npm": "2506585151",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "IT Enthusiast, Third semester, Studying at Fasilkom UI"
        ),
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
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def show_projects(request):
    json_response = get_projects_json(request)
    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]

    title_query = request.GET.get("title", "").strip()
    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)


def create_project(request):
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


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")
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
