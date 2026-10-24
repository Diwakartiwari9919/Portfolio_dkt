from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import PortfolioProfile, Qualification, private_storage


class PortfolioPageTests(TestCase):
    def test_empty_portfolio_prompts_owner_to_set_it_up(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Set up your portfolio')

    def test_portfolio_shows_profile_and_qualification_details(self):
        PortfolioProfile.objects.create(
            full_name='Taylor Example',
            headline='Designer and developer',
            email='taylor@example.com',
        )
        Qualification.objects.create(
            qualification='Bachelor of Science',
            institution='Example University',
            field_of_study='Computer Science',
            status=Qualification.Status.COMPLETED,
            end_year=2025,
            marks_or_grade='First class',
        )

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Taylor Example')
        self.assertContains(response, 'Example University')
        self.assertContains(response, 'First class')

    def test_marksheet_download_requires_staff_login(self):
        qualification = Qualification.objects.create(
            qualification='Higher Secondary',
            institution='Example School',
        )

        response = self.client.get(f'/marksheet/{qualification.pk}/')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_staff_can_download_private_marksheet(self):
        with TemporaryDirectory() as upload_dir:
            original_location = private_storage.location
            private_storage.location = upload_dir
            try:
                qualification = Qualification.objects.create(
                    qualification='Higher Secondary',
                    institution='Example School',
                    marksheet=SimpleUploadedFile(
                        'marks.pdf',
                        b'%PDF-1.4 test document',
                        content_type='application/pdf',
                    ),
                )
                staff = get_user_model().objects.create_user(
                    username='portfolio-admin',
                    password='test-password',
                    is_staff=True,
                )
                self.client.force_login(staff)

                response = self.client.get(f'/marksheet/{qualification.pk}/')

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response['Content-Type'], 'application/pdf')
                self.assertIn('attachment;', response['Content-Disposition'])
                self.assertEqual(b''.join(response.streaming_content), b'%PDF-1.4 test document')
            finally:
                private_storage.location = original_location

    def test_missing_resume_returns_not_found(self):
        PortfolioProfile.objects.create(full_name='Taylor Example')

        response = self.client.get('/resume/')

        self.assertEqual(response.status_code, 404)
