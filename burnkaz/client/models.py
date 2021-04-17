from django.db import models


class Client(models.Model):
    user = models.OneToOneField('userauth.User', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, null=True, blank=True)

class DevClientInContact(models.Model):
    dev_id = models.ManyToManyField("developer.Developer", null=True)
    dev_perm = models.BooleanField(null=True, default=False)
    client_id = models.ForeignKey(to="Client", on_delete=models.CASCADE)
