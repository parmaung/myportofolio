from django.forms import ModelForm, NumberInput, Select, TextInput, Textarea, URLInput

from main.models import Education, Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "link",
            "thumbnail",
        ]
        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "link": "URL Proyek",
            "thumbnail": "URL Gambar Proyek",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, PostgreSQL, React",
                }
            ),
            "link": URLInput(
                attrs={
                    "placeholder": "https://github.com/username/project",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution_name",
            "level",
            "field_of_study",
            "gpa",
            "start_year",
            "end_year",
            "description",
        ]
        labels = {
            "institution_name": "Nama Institusi",
            "level": "Jenjang Pendidikan",
            "field_of_study": "Jurusan/Program Studi",
            "gpa": "IPK/Nilai",
            "start_year": "Tahun Mulai",
            "end_year": "Tahun Selesai",
            "description": "Deskripsi",
        }
        widgets = {
            "institution_name": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "level": Select(),
            "field_of_study": TextInput(
                attrs={
                    "placeholder": "Sistem Informasi",
                }
            ),
            "gpa": NumberInput(
                attrs={
                    "placeholder": "3.75",
                    "step": "0.01",
                    "min": "0",
                    "max": "4",
                }
            ),
            "start_year": NumberInput(
                attrs={
                    "placeholder": "2024",
                    "min": "1900",
                    "max": "2100",
                }
            ),
            "end_year": NumberInput(
                attrs={
                    "placeholder": "2028 (kosongkan jika masih berlangsung)",
                    "min": "1900",
                    "max": "2100",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalaman pendidikanmu",
                    "rows": 3,
                }
            ),
        }
