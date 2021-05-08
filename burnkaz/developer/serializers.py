from rest_framework import serializers

from userauth.serializers import UserSerializer
from .models import Skills, Stacks, Developer, DeveloperService, \
    Rating, \
    Review, \
    ImageTab, Favorites, Feedback
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
    # average_rating = serializers.IntegerField(source='get_count_avg')
    # count_rating = serializers.IntegerField(source='get_count_avg')
    # communication = serializers.IntegerField(source='get_communication')
    # quality = serializers.IntegerField(source='get_quality')
    # truth_review = serializers.IntegerField(source='get_truth')
    rating_average = serializers.SerializerMethodField("get_rating_average")
    rating_count = serializers.SerializerMethodField("get_rating_count")
    rating_communication = serializers.SerializerMethodField('get_rating_communication')
    rating_quality = serializers.SerializerMethodField('get_rating_quality')
    rating_truth_review = serializers.SerializerMethodField('get_rating_truth_review')
    print(1)

    class Meta:
        model = Rating
        fields = ["rating_average", 'rating_count',
                  'rating_communication', 'rating_quality',
                  'rating_truth_review']

    def quality_validate(self, quality):
        if ['/','%'] in quality:
            raise serializers.ValidationError('invalid character')

    def get_rating_average(self, obj):
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

    def get_rating_count(self, obj):
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

    def get_rating_truth_review(self, obj):
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

    def get_rating_quality(self, obj):
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

    def get_truth_review(self, obj):
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
    is_favorite = serializers.SerializerMethodField('get_favorite')
    class Meta:
        model = Developer
        fields = ['id', "user", "stacks_id", "skills_id",
                  "rating", "rating_count", "price",
                  "is_favorite"]

    def get_favorite(self, obj):
        try:
            # user = self.context['request'].user
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
            fav = Favorites.objects.get(developer=obj, user=user)
            return True
        except:
            return False

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
    @staticmethod
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
    rating = RatingSerializer(many=True, read_only=True)
    review = ReviewSerializer(many=True, read_only=True)
    dev_service = DeveloperServiceSerializer(many=False, read_only=True)
    is_favoritex = serializers.BooleanField(read_only=True)
    class Meta:
        model = Developer
        fields = ['id', "user", "education", "dev_service",
                  "stacks_id", "skills_id", "rating", "review",
                  "work_experience", "about",
                  "is_favoritex"]

    def restore_object(self, attrs, instance=None):
        # is_favorite = attrs.pop('is_favoritex')
        instance = super(FullInfoDeveloperSerializer, self).restore_object(attrs, instance=instance)
        return instance


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

"""
REVIEW
"""

class ReviewSerializer(serializers.ModelSerializer):
    # user_id = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Review
        fields = ['text', 'developer']



class RatingSerializer(serializers.ModelSerializer):
    # user_id = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Rating
        fields = ['communication', 'quality', 'truth_review',
                    'developer']

class RatingDevSerializer(serializers.ModelSerializer):
    # user_id = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Rating
        fields = ['communication', 'quality', 'truth_review']

    def create(self, validated_data):
        developer = validated_data.get('developer_id')
        ratings = Rating.objects.create(**validated_data)
        dev = Developer.objects.get(id=developer)
        dev.rating_id = ratings.id
        # for building_data in buildings_data:
        #     Building.objects.create(building_group=building_group, **building_data)
        return ratings


class ReviewRatingSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(many=False, read_only=True)
    rating_id = RatingSerializer
    review_id = ReviewSerializer

    class Meta:
        model = Review
        fields = ['user_id', 'rating']


class FeedbackSerializer(serializers.ModelSerializer):
    rating_id = RatingSerializer()
    review_id = ReviewSerializer()
    user_id = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Feedback
        fields = ['developer_id', 'rating_id', 'review_id', 'user_id']

    # def create(self, validated_data):
    #     review = validated_data.pop('review_id')
    #     order = Review.objects.create(**review)
    #     review = validated_data.pop('rating_id')
    #     print(review)
    #     order = Rating.objects.create(**review)
    #     # instance = Equipment.objects.create(**validated_data)
    #     # Assignment.objects.create(Order=order, Equipment=instance)
    #     return order