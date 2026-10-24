from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import PortfolioProfile, Qualification


def portfolio(request):
    profile = PortfolioProfile.objects.first()
    qualifications = Qualification.objects.all()
    return render(
        request,
        'firstApp/portfolio.html',
        {
            'profile': profile,
            'qualifications': qualifications,
            'current_year': timezone.now().year,
        },
    )


def resume_download(request):
    profile = PortfolioProfile.objects.first()
    if not profile or not profile.resume:
        raise Http404('No resume has been uploaded.')
    return FileResponse(
        profile.resume.open('rb'),
        as_attachment=True,
        filename=profile.resume.name.rsplit('/', 1)[-1],
        content_type='application/pdf',
    )


@staff_member_required
def marksheet_download(request, qualification_id):
    qualification = get_object_or_404(Qualification, pk=qualification_id)
    if not qualification.marksheet:
        raise Http404('No marksheet has been uploaded.')
    extension = qualification.marksheet.name.rsplit('.', 1)[-1].lower()
    content_types = {
        'pdf': 'application/pdf',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
    }
    return FileResponse(
        qualification.marksheet.open('rb'),
        as_attachment=True,
        filename=qualification.marksheet.name.rsplit('/', 1)[-1],
        content_type=content_types.get(extension, 'application/octet-stream'),
    )
