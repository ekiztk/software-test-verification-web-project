import requests
import time
from datetime import datetime
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import ImageUploadModel
from .forms import ImageUploadForm
from django.urls import reverse
from django.http import HttpRequest
from .views import upload_image
from bs4 import BeautifulSoup

#test for image upload
class TestImageUploadModel(TestCase):
    def setUp(self):
        # Create a simple image file for testing
        self.current_time_millis = int(time.mktime(datetime.now().timetuple()) * 1000)
        image = SimpleUploadedFile(name=f'test_image_{self.current_time_millis}.jpg', content=b'\x00\x01\x02\x03', content_type='image/jpeg')
        # Create an instance of the model
        self.image_upload = ImageUploadModel.objects.create(image=image)

    def test_image_field(self):
        image_upload = ImageUploadModel.objects.get(id=self.image_upload.id)
        self.assertEqual(image_upload.image.name, f'images/test_image_{self.current_time_millis}.jpg')

#test for image upload form
class TestImageUploadForm(TestCase):
    def setUp(self):
        # Create a simple image file for testing
        image = SimpleUploadedFile(name='test_image2.jpg', content=b'\x00\x01\x02\x03', content_type='image/jpeg')

        # Create an instance of the form
        self.form_data = {
            'low_h': 0,
            'low_v': 0,
            'low_s': 199,
            'high_h': 180,
            'high_v': 50,
            'high_s': 255,
        }
        self.form_files = {
            'image': image,
        }

        self.client = Client()

    def test_form_fields(self):
        try:
            response = self.client.post('', data=self.form_data, files=self.form_files)
            self.assertEqual(response.status_code, 200)
        except Exception as e:
            self.fail(f'Test failed due to: {str(e)}')

#test for load time
class TestHomePageLoadTime(TestCase):
    def test_load_time(self):
        url = "http://127.0.0.1:8000/"
        max_time = 5
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        load_time = end_time - start_time
        self.assertLessEqual(load_time, max_time, f"Yükleme süresi {max_time} saniyeyi aştı: {load_time} saniye")

#test for html
class TestHTML(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_exists(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  
        response = upload_image(request)  
        html = response.content.decode("utf8")  
        self.assertTrue(html.startswith("<html>"))  
        self.assertTrue(html.endswith("</html>"))

    def test_home_page_has_correct_elements(self):
        request = HttpRequest()
        response = upload_image(request)
        html = response.content.decode('utf8')
        self.assertIn("<h1>Console 1 Web App</h1>", html)
        self.assertIn("</header>", html)
        self.assertIn("<main>", html)
        self.assertIn("</main>", html)
        
    def test_home_page_css(self):
        request = HttpRequest()
        response = upload_image(request)
        soup = BeautifulSoup(response.content, 'html.parser')

        header = soup.find('header')
        self.assertIsNotNone(header)
        self.assertEqual(header['style'], 'background-color: #f8f9fa; padding: 12px; text-align: center; border-bottom: 1px solid #e7e7e7;')

    def test_upload_page_form_exits(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertIn('<form method="POST" enctype="multipart/form-data">', html)
        self.assertIn('<button type="submit">Yükle</button>', html)

    def test_upload_page_inputs_exits(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertIn('<h2>Resim Yükle</h2>', html)
        self.assertIn('<input type="hidden" name="csrfmiddlewaretoken"', html)
        self.assertIn('<input type="file" name="image" accept="image/*" required id="id_image">', html)
        self.assertIn('<input type="number" name="low_h" value="0" min="0" max="255" required id="id_low_h">', html)
        self.assertIn('<input type="number" name="low_v" value="0" min="0" max="255" required id="id_low_v">', html)
        self.assertIn('<input type="number" name="low_s" value="199" min="0" max="255" required id="id_low_s">', html)
        self.assertIn('<input type="number" name="high_h" value="180" min="0" max="255" required id="id_high_h">', html)
        self.assertIn('<input type="number" name="high_v" value="50" min="0" max="255" required id="id_high_v">', html)
        self.assertIn('<input type="number" name="high_s" value="255" min="0" max="255" required id="id_high_s">', html)

    def test_form_submission(self):
        current_time_millis = int(time.mktime(datetime.now().timetuple()) * 1000)
        image_content = b"image content"
        image_file = SimpleUploadedFile(f'test_image_{current_time_millis}.jpg', image_content, content_type="image/jpeg")

        form_data = {
            "image": image_file,
            "low_h": 0,
            "low_v": 0,
            "low_s": 199,
            "high_h": 180,
            "high_v": 50,
            "high_s": 255,
        }

        response = self.client.post("http://127.0.0.1:8000/", form_data)

        # Check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)