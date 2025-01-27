from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_pic_base64 = models.TextField(blank=True, null=True)  # Store Base64 string

    def set_profile_pic(self, image_file):
        import base64
        from io import BytesIO
        from PIL import Image
        
        # Convert image to base64
        image = Image.open(image_file)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        self.profile_pic_base64 = img_str
        self.save()
