from rest_framework import serializers

from userauth.serializers import UserSerializer
from .models import Skills, Stacks, Developer, DeveloperService, \
    Rating, \
    Review, \
    ImageTab, Favorites
from userauth.models import User, City
from devutils.serializers import StacksSerializer,\
                                 StackTitleSerializer,\
                                 SkillTitleSerializer,\
                                 SkillsSerializer
from client.models import DevClientInContact, Client


class ReviewSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField('get_review_count')
    user = serializers.SerializerMethodField('get_name')
    review = serializers.SerializerMethodField('get_review')
    rating = serializers.SerializerMethodField('get_rating')

    class Meta:
        model = Review
        fields = ['review_count', 'user', 'text', 'review', 'rating']
    def get_name(self, obj):
        dev = Developer.objects.get(obj)
        return dev.user.name
    def get_review_count(self, obj):
        review = Review.objects.filter(developer=obj).count()
        return review
    def get_review(self, obj):
        review = Review.objects.filter(developer=obj)
        return review.text
    def get_rating(self, obj):
        rating = Rating.objects.filter(developer=obj)
        return (rating.communication+rating.quality+rating.truth_review)/3

class RatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField("get_rating_avg")
    count_rating = serializers.SerializerMethodField('get_count_avg')
    communication = serializers.SerializerMethodField('get_communication')
    quality = serializers.SerializerMethodField('get_quality')
    truth_review = serializers.SerializerMethodField('get_truth')

    class Meta:
        model = Rating
        fields = ["average_rating", 'count_rating', 'communication', 'quality', 'truth_review']

    def get_count_avg(self, obj):
        try:
            rating = Rating.objects.filter(developer=obj)
            sum_rate = 0
            count_rate = 0
            for rate in rating:
                all_rate = (rate.communication + rate.quality + rate.truth_review) / 3
                sum_rate += all_rate
                count_rate += 1
            if count_rate == 0:
                count_rate = 0
            return count_rate
        except:
            return 0

    def get_rating_avg(self, obj):
        try:
            rating = Rating.objects.filter(developer=obj)
            sum_rate = 0
            count_rate = 0
            for rate in rating:
                all_rate = (rate.communication + rate.quality + rate.truth_review) / 3
                sum_rate += all_rate
                count_rate += 1
            if count_rate > 0:
                avg_rating = sum_rate / count_rate
            else:
                avg_rating = 0
            return avg_rating
        except:
            return 0

    def get_communication(self, obj):
        try:
            rating = Rating.objects.filter(developer=obj)
            sum_rate = 0
            count_rate = 0
            for rate in rating:
                sum_rate += rate.communication
                count_rate += 1
            if count_rate > 0:
                avg_communication = sum_rate/count_rate
            else:
                avg_communication = 0
            return avg_communication
        except:
            return 0

    def get_quality(self, obj):
        try:
            rating = Rating.objects.filter(developer=obj)
            sum_rate = 0
            count_rate = 0
            for rate in rating:
                sum_rate += rate.quality
                count_rate += 1
            if count_rate > 0:
                avg_quality = sum_rate/count_rate
            else:
                avg_quality = 0
            return avg_quality
        except:
            return 0

    def get_truth(self, obj):
        try:
            rating = Rating.objects.filter(developer=obj)
            sum_rate = 0
            count_rate = 0
            for rate in rating:
                sum_rate += rate.truth_review
                count_rate += 1
            if count_rate > 0:
                avg_truth_review = sum_rate/count_rate
            else:
                avg_truth_review = 0
            return avg_truth_review
        except:
            return 0

class DevelopersSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    stacks_id = StacksSerializer(many=False, read_only=True)
    skills_id = SkillsSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField("get_rating_avg")
    rating_count = serializers.SerializerMethodField("get_rating_count")
    price = serializers.SerializerMethodField('get_price')

    class Meta:
        model = Developer
        fields = ['id', "user", "stacks_id", "skills_id",
                  "rating", "rating_count", "price"]

    def get_rating_count(self, obj):
        rating = Rating.objects.filter(developer=obj)
        sum_rate = 0
        count_rate = 0
        for rate in rating:
            all_rate = (rate.communication + rate.quality + rate.truth_review) / 3
            sum_rate += all_rate
            count_rate += 1
        if count_rate == 0:
            count_rate = 0
        return count_rate

    def get_rating_avg(self, obj):
        rating = Rating.objects.filter(developer=obj)
        sum_rate = 0
        count_rate = 0
        for rate in rating:
            all_rate = (rate.communication + rate.quality + rate.truth_review)/3
            sum_rate += all_rate
            count_rate += 1
        if count_rate > 0:
            avg_rating = sum_rate / count_rate
        else:
            avg_rating = None
        return avg_rating

    def get_price(self, obj):
        try:
            service = DeveloperService.objects.get(developer=obj)
            return service.price
        except:
            return None

class StackDeveloperSerializer(serializers.ModelSerializer):
    developer_list_stacks = DevelopersSerializer(many=True, read_only=True)
    class Meta:
        model = Stacks
        fields = ['id', 'title', 'developer_list_stacks']
    #
    # def get_stack_dev(self, obj):
    #     stacks = Stacks.objects.all()
    #     for stack in stacks:
    #         developer = Developer.objects.filter(stacks_id=stack)
    #         return DevelopersSerializer(instance=developer)

class DeveloperServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeveloperService
        fields = ['id', 'service_title', 'service_description', 'price', 'price_fix']


class FullInfoDeveloperSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    # birth_date = serializers.DateField(format="%d.%m.%Y")
    # city = serializers.CharField(read_only=False,write_only=False)
    stacks_id = StacksSerializer(many=False, read_only=True)
    skills_id = SkillsSerializer(many=True, read_only=True)
    # rating = serializers.SerializerMethodField("get_rating_avg")
    # rating_count = serializers.SerializerMethodField("get_rating_count")
    # price = serializers.SerializerMethodField('get_price')
    rating = RatingSerializer(many=False, read_only=True)
    review_count = ReviewSerializer(many=True, read_only=True)
    dev_service = DeveloperServiceSerializer(many=False, read_only=True)

    class Meta:
        model = Developer
        fields = ['id', "user", "education", "dev_service",
                  "stacks_id", "skills_id", "rating",
                  "work_experience", "review_count", "about", ]


    def get_rating_count(self, obj):
        rating = Rating.objects.filter(developer=obj)
        sum_rate = 0
        count_rate = 0
        for rate in rating:
            all_rate = (rate.communication + rate.quality + rate.truth_review) / 3
            sum_rate += all_rate
            count_rate += 1
        if count_rate == 0:
            count_rate = 0
        return count_rate

    def get_rating_avg(self, obj):
        rating = Rating.objects.filter(developer=obj)
        sum_rate = 0
        count_rate = 0
        for rate in rating:
            all_rate = (rate.communication + rate.quality + rate.truth_review)/3
            sum_rate += all_rate
            count_rate += 1
        if count_rate > 0:
            avg_rating = sum_rate / count_rate
        else:
            avg_rating = None
        return avg_rating

    def get_price(self, obj):
        service = DeveloperService.objects.get(developer=obj)
        return service.price

class DeveloperContactsSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField('get_name')

    class Meta:
        model = DevClientInContact
        fields = ['id', 'client_id', 'client', 'dev_perm']

    def get_name(self, obj):
        client = Client.objects.get(id=obj.client_id.id)
        user = {
            "name": client.user.name,
            "surname": client.user.surname
        }
        return user

class FavoritesSerializer(serializers.ModelSerializer):
    developer = DevelopersSerializer(many=False, read_only=True)

    class Meta:
        model = Favorites
        fields = ['developer', ]

class ReviewSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Review
        fields = ['text', 'developer', 'user_id']

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['communication', 'quality', 'truth_review',
                    'developer', 'user_id']



























