from django.db import models

class Permission(models.Model):
    permission_group = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    min_level = models.CharField(max_length=100, default='STATION')
    
    def __str__(self):
        return self.permission_group + "-" + self.action