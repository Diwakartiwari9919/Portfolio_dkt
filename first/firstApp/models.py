from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class PrivateUploadStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('location', settings.MEDIA_ROOT)
        super().__init__(*args, **kwargs)


private_storage = PrivateUploadStorage()


def validate_upload_size(upload):
    if upload.size > 10 * 1024 * 1024:
        raise ValidationError('Files must be 10 MB or smaller.')


class PortfolioProfile(models.Model):
    full_name = models.CharField(max_length=120)
    headline = models.CharField(max_length=180, blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=120, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    resume = models.FileField(
        upload_to='resumes/',
        storage=private_storage,
        blank=True,
        validators=[FileExtensionValidator(['pdf']), validate_upload_size],
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'portfolio profile'
        verbose_name_plural = 'portfolio profile'

    def __str__(self):
        return self.full_name


class Qualification(models.Model):
    class Status(models.TextChoices):
        COMPLETED = 'completed', 'Completed'
        IN_PROGRESS = 'in_progress', 'In progress'
        PLANNED = 'planned', 'Planned'

    qualification = models.CharField(max_length=160)
    institution = models.CharField(max_length=180)
    field_of_study = models.CharField(max_length=160, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.COMPLETED,
    )
    start_year = models.PositiveSmallIntegerField(blank=True, null=True)
    end_year = models.PositiveSmallIntegerField(blank=True, null=True)
    marks_or_grade = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    marksheet = models.FileField(
        upload_to='marksheets/',
        storage=private_storage,
        blank=True,
        validators=[
            FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg']),
            validate_upload_size,
        ],
    )
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-end_year', 'qualification']

    def __str__(self):
        return f'{self.qualification} — {self.institution}'

    @property
    def year_range(self):
        if self.start_year and self.end_year:
            return f'{self.start_year} – {self.end_year}'
        if self.end_year:
            return str(self.end_year)
        if self.start_year:
            return f'Since {self.start_year}'
        if self.status == self.Status.IN_PROGRESS:
            return 'In progress'
        if self.status == self.Status.PLANNED:
            return 'Planned'
        return ''
