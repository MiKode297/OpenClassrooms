from django.db import models

class Path(models.Model):
    name = models.CharField(max_length=200)
    reference_id = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Project(models.Model):
    name = models.CharField(max_length=200)
    reference_id = models.CharField(max_length=200)
    path = models.ForeignKey(Path, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Course(models.Model):
    name = models.CharField(max_length=200)
    reference_id = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
