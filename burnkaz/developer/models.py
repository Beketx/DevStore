from django.db import models
from userauth.models import User


class Stacks(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.title

class Skills(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.title

class Developer(models.Model):
    user = models.OneToOneField('userauth.User', on_delete=models.CASCADE)
    education = models.CharField(max_length=140, null=True)
    about = models.CharField(max_length=255, null=True)
    work_experience = models.CharField(max_length=255, null=True)
    dev_service = models.OneToOneField(to="DeveloperService", on_delete=models.CASCADE, null=True)
    stacks_id = models.ManyToManyField(Stacks, related_name="developer_list_stacks")
    skills_id = models.ManyToManyField(Skills, related_name="developer_list_skills")
    
    def __str__(self):
        return self.user.email

class Rating(models.Model):
    communication = models.FloatField(null=True)
    quality = models.FloatField(null=True)
    truth_review = models.FloatField(null=True)
    developer = models.ForeignKey(to="Developer", on_delete=models.CASCADE, null=True)
    user_id = models.IntegerField(null=True)

    @property
    def rating_count(self, dev):
        return Rating.objects.filter(developer=dev).count()

class Review(models.Model):
    text = models.TextField(null=True)
    developer = models.ForeignKey(to="Developer", on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey("userauth.User", on_delete=models.CASCADE, null=True)

class ImageTab(models.Model):
    developer = models.ForeignKey(to="Developer", on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500, null=True)
    image_type = models.ForeignKey(to="ImageType", on_delete=models.CASCADE)


class ImageType(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type_code = models.CharField(unique=True, max_length=20, blank=True, null=True)
    # front_photo = models.CharField(max_length=100, null=True)
    # avatar = models.CharField(max_length=100, null=True)
    # passport = models.CharField(max_length=100, null=True)

class DeveloperService(models.Model):
    service_title = models.CharField(max_length=100, null=True)
    service_description = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True)
    price_fix = models.BooleanField(default=True)


