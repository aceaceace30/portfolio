from rest_framework import serializers
from portfolio.models import (
    About, Project, ProjectImage, Skill,
    JobExperience, Task, Testimonial
)


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['pk', 'name', 'value']


class ProjectImageSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(slug_field='slug', queryset=Project.objects.all())

    class Meta:
        model = ProjectImage
        fields = ['project', 'image', 'description', 'is_cover']


class ProjectSerializer(serializers.ModelSerializer):
    project_images = ProjectImageSerializer(read_only=True, many=True)
    next_project_url = serializers.ReadOnlyField(source='next_project')
    previous_project_url = serializers.ReadOnlyField(source='previous_project')

    class Meta:
        model = Project
        fields = ['url', 'name', 'slug', 'description', 'back_end', 'front_end',
                  'classification', 'git_link', 'website_link', 'ordering',
                  'next_project_url', 'previous_project_url', 'project_images']
        extra_kwargs = {
            'url': {'view_name': 'api-project-detail', 'lookup_field': 'slug'}
        }


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['description', 'active']


class JobExperienceSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True, many=True)

    class Meta:
        model = JobExperience
        fields = ['job_title', 'company', 'duration', 'task', 'ordering', 'active']


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['name', 'positive_remarks', 'platform', 'project_description',
                  'project_year', 'active']
