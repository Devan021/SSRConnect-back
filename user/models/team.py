from django.db import models


class Team(models.Model):
    teamID = models.CharField(max_length=20, unique=True, null=True)
    mentor = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_mentor')
    project = models.ForeignKey('project.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_project')

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.teamID
