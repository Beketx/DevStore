from django.db import models
from userauth.models import User
from utils.developer_pagination.pagination import developer_photos_path, developer_photos_size, developer_file_extension


class Stacks(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.title

class Skills(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'


class Developer(models.Model):
    user = models.OneToOneField('userauth.User', on_delete=models.CASCADE)
    education = models.CharField(max_length=140, null=True)
    about = models.CharField(max_length=255, null=True)
    work_experience = models.CharField(max_length=255, null=True)
    dev_service = models.OneToOneField(to="DeveloperService", on_delete=models.CASCADE, null=True)
    stacks_id = models.ForeignKey(Stacks, on_delete=models.CASCADE, related_name="developer_list_stacks", null=True)
    skills_id = models.ManyToManyField(Skills, related_name="developer_list_skills")
    # rating_id = models.ManyToManyField(to="Rating", related_name='developer_rating')

    @property
    def isFavorite(self):
        if Favorites.objects.get(developer_id=self.id):
            return True

    def __str__(self):
        return self.user.email

class FavoriteManager(models.QuerySet):

    def for_user(self, user):
        return self.filter(user=user).order_by('developer')

class TrueFavorites(models.Manager):

    def get_queryset(self):
        return self.objects.filter(favorite_bool=True)

class NotFavorites(models.Manager):

    def get_queryset(self):
        return self.objects.filter(favorite_bool=False)

class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, null=True, blank=True)
    favorite_bool = models.BooleanField(default=False, null=True, blank=True)

    favorite_devs = TrueFavorites()
    not_favorite_devs = NotFavorites()
    objects = FavoriteManager.as_manager()

class RatingManager(models.Manager):

    def rating_count(self, dev):
        self.objects.filter(developer=dev).count()

class Rating(models.Model):
    communication = models.FloatField(null=True)
    quality = models.FloatField(null=True)
    truth_review = models.FloatField(null=True)
    developer = models.ForeignKey(to="Developer", on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey("userauth.User", on_delete=models.CASCADE, null=True)

    objects = RatingManager()

    @property
    def rating_count(self, dev):
        return self.objects.filter(developer=dev).count()

    # @property
    # def get_count_avg(self, obj):
    #     try:
    #         rating = self.objects.filter(developer=obj)
    #         sum_rate = 0
    #         count_rate = 0
    #         for rate in rating:
    #             all_rate = (rate.communication + rate.quality + rate.truth_review) / 3
    #             sum_rate += all_rate
    #             count_rate += 1
    #         if count_rate == 0:
    #             count_rate = 0
    #         return count_rate
    #     except:
    #         return 0
    #
    # @property
    # def get_rating_avg(self, obj):
    #     try:
    #         rating = self.objects.filter(developer=obj)
    #         sum_rate = 0
    #         count_rate = 0
    #         for rate in rating:
    #             all_rate = (rate.communication + rate.quality + rate.truth_review) / 3
    #             sum_rate += all_rate
    #             count_rate += 1
    #         if count_rate > 0:
    #             avg_rating = sum_rate / count_rate
    #         else:
    #             avg_rating = 0
    #         return avg_rating
    #     except:
    #         return 0
    #
    # @property
    # def get_communication(self, obj):
    #     try:
    #         rating = self.objects.filter(developer=obj)
    #         sum_rate = 0
    #         count_rate = 0
    #         for rate in rating:
    #             sum_rate += rate.communication
    #             count_rate += 1
    #         if count_rate > 0:
    #             avg_communication = sum_rate/count_rate
    #         else:
    #             avg_communication = 0
    #         return avg_communication
    #     except:
    #         return 0
    #
    # @property
    # def get_quality(self, obj):
    #     try:
    #         rating = self.objects.filter(developer=obj)
    #         sum_rate = 0
    #         count_rate = 0
    #         for rate in rating:
    #             sum_rate += rate.quality
    #             count_rate += 1
    #         if count_rate > 0:
    #             avg_quality = sum_rate/count_rate
    #         else:
    #             avg_quality = 0
    #         return avg_quality
    #     except:
    #         return 0
    #
    # @property
    # def get_truth(self, obj):
    #     try:
    #         rating = self.objects.filter(developer=obj)
    #         sum_rate = 0
    #         count_rate = 0
    #         for rate in rating:
    #             sum_rate += rate.truth_review
    #             count_rate += 1
    #         if count_rate > 0:
    #             avg_truth_review = sum_rate/count_rate
    #         else:
    #             avg_truth_review = 0
    #         return avg_truth_review
    #     except:
    #         return 0

    # @property
    # def avg_rating(self):
    #     return

class ReviewManager(models.Manager):

    def review_count(self, dev):
        self.objects.filter(developer=dev).count()

class Review(models.Model):
    text = models.TextField(null=True)
    developer = models.ForeignKey(to="Developer", on_delete=models.CASCADE, null=True, related_name='developer')
    user_id = models.ForeignKey("userauth.User", on_delete=models.CASCADE, null=True)

    objects = ReviewManager()

class FeedbackManager(models.QuerySet):
    def get_related(self):
        return self.select_related('developer')

class Feedback(models.Model):
    developer_id = models.ForeignKey(to="Developer", on_delete=models.CASCADE, null=True)
    rating_id = models.ForeignKey(to="Rating", on_delete=models.CASCADE, null=True)
    review_id = models.ForeignKey(to="Review", on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey("userauth.User", on_delete=models.CASCADE, null=True)

    objects = FeedbackManager.as_manager()

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

class DeveloperImages(models.Model):
    developer = models.ForeignKey(to="Developer", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=developer_photos_path,
                                  validators=[developer_photos_size,
                                              developer_file_extension],
                                   blank=True,
                                   null=True)
    image_type = models.ForeignKey(to="ImageType", on_delete=models.CASCADE)

class DeveloperService(models.Model):
    service_title = models.CharField(max_length=100, null=True)
    service_description = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True)
    price_fix = models.BooleanField(default=True)


