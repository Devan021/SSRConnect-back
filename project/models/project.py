from django.db import models
from django.utils import timezone

IN_PROGRESS = 1
UNDER_REVIEW = 2
COMPLETED = 3
STATUS = [
    (IN_PROGRESS, "In Progress"),
    (UNDER_REVIEW, "Under Review"),
    (COMPLETED, "Completed"),
]


class Project(models.Model):
    name = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=False)
    links = models.JSONField(null=True, blank=True)
    attachment = models.FileField(upload_to='project/attachment/', null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    cover = models.ImageField(upload_to='project/cover/', null=True, blank=True)
    collaborators = models.JSONField(null=True, blank=True)
    team = models.OneToOneField(
        'user.Team',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='project_team'
    )
    proposal = models.OneToOneField(
        'project.Proposal',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='project_proposal'
    )
    isPublished = models.BooleanField(default=False)
    current_status = models.TextField(null=True, blank=True)
    status_updated_at = models.DateTimeField()
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=IN_PROGRESS,
    )

    def clean(self):
        if self.name and not self.slug:
            # @TODO: Handle slug generation
            self.slug = self.name.lower().replace(" ", "-")

        if self.current_status:
            self.status_updated_at = timezone.now()

        if self.status == COMPLETED:
            self.end_date = timezone.now()

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
