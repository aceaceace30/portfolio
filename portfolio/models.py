import os

from datetime import date, datetime

from ckeditor.fields import RichTextField
from django.core.paginator import Paginator
from django.db import models
from django.urls import reverse


class Project(models.Model):
    COMPANY = 'company'
    FREELANCE = 'freelance'
    PERSONAL = 'personal'

    CLASSIFICATION_CHOICES = (
        (COMPANY, 'Company'),
        (FREELANCE, 'Freelance'),
        (PERSONAL, 'Personal'),
    )

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = RichTextField(null=True, blank=True)
    back_end = models.CharField(max_length=255, verbose_name='Back-End Technology')
    front_end = models.CharField(max_length=255, verbose_name='Front-End Technology')
    classification = models.CharField(choices=CLASSIFICATION_CHOICES, max_length=30)
    git_link = models.URLField(null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    ordering = models.PositiveIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portfolio:project_details', kwargs={'slug': self.slug})

    def get_previous_or_next_project(self, p_or_n):
        try:
            if p_or_n == 'p':
                return Project.objects.get(ordering=self.ordering-1)
            elif p_or_n == 'n':
                return Project.objects.get(ordering=self.ordering+1)
        except self.DoesNotExist:
            return None


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_images')
    image = models.ImageField(upload_to='project_images')
    description = models.TextField(null=True, blank=True)
    is_cover = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['project']

    def __str__(self):
        return f'{self.project.name} - {self.get_image_name}'

    @property
    def get_image_name(self):
        return os.path.basename(self.image.name)


class About(models.Model):
    name = models.CharField(max_length=150, unique=True)
    value = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @staticmethod
    def get_age(birthdate):
        try:
            birthdate = datetime.strptime(birthdate, '%b %d, %Y')
            today = date.today()
            return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        except ValueError:
            return '----'


class Skill(models.Model):
    name = models.CharField(max_length=150, unique=True)
    value = models.CharField(max_length=150)
    ordering = models.PositiveIntegerField(unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.name

    @staticmethod
    def get_splitted_skill_set():
        skills = Skill.objects.filter(active=True)
        paginator = Paginator(skills, skills.count() / 2)
        return paginator.page(1), paginator.page(2)


class Task(models.Model):
    description = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class JobExperience(models.Model):
    job_title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    duration = models.CharField(max_length=150)
    task = models.ManyToManyField(Task, through='JobExperienceTask', related_name='job_experiences')
    ordering = models.PositiveIntegerField(unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return f'{self.job_title} - {self.company}'


class JobExperienceTask(models.Model):
    job_experience = models.ForeignKey(JobExperience, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)


class Message(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.email} - {self.subject}'
