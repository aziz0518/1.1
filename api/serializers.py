from rest_framework import serializers
from .models import Author, Book
from datetime import date, timezone

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def validate_birth_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Tug‘ilgan sana kelajakda bo‘lishi mumkin emas.")
        return value

class BookSerializer(serializers.ModelSerializer):
    author_full_name = serializers.SerializerMethodField(read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Book
        fields = '__all__'

    def get_author_full_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Sarlavha kamida 3 ta belgidan iborat bo‘lishi kerak.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Narx manfiy bo‘lishi mumkin emas.")
        return value

    def validate(self, data):
        author = data.get('author')
        published_date = data.get('published_date')

        if author and published_date and published_date < author.birth_date:
            raise serializers.ValidationError("Nashr sanasi muallif tug‘ilgan sanasidan oldin bo‘lishi mumkin emas.")
        return data
