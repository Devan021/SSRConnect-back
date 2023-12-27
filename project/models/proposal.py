from django.db import models
from django.utils import timezone

IN_PROGRESS = 1
APPROVED = 2
REJECTED = 3
FROZEN = 4

STATE = [
    (1, 'In Progress'),
    (2, 'Approved'),
    (3, 'Rejected'),
    (4, 'Frozen')
]


class Proposal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    attachment = models.FileField(upload_to='proposal/', null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()
    state = models.CharField(
        max_length=2,
        choices=STATE,
        default=IN_PROGRESS,
    )
    remarks = models.TextField(null=True, blank=True)
    remark_updated_at = models.DateTimeField(null=True, blank=True)
    team = models.ForeignKey('user.Team', on_delete=models.CASCADE)

    @property
    def isUpdated(self):
        return self.updated_at > self.remark_updated_at

    def clean(self):
        self.updated_at = timezone.now()

        if self.remarks:
            self.remark_updated_at = timezone.now()

        if self.state == APPROVED:
            self.remarks = None
            self.remark_updated_at = timezone.now()
            Proposal.objects.filter(team=self.team, state__exact=IN_PROGRESS).exclude(id=self.id).update(state=FROZEN)

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title