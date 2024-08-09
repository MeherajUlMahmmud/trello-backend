from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'user_control.UserModel', related_name='%(class)s_created_by',
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    updated_by = models.ForeignKey(
        'user_control.UserModel', related_name='%(class)s_updated_by',
        on_delete=models.SET_NULL, null=True, blank=True,
    )

    objects = models.Manager()

    class Meta:  # This is an abstract class and will not be created in the database
        abstract = True


class ContactUsModel(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    is_checked = models.BooleanField(default=False)

    class Meta:
        db_table = 'contact_us'
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.name


class RequestLog(models.Model):
    user = models.ForeignKey(
        'user_control.UserModel', on_delete=models.CASCADE,
        null=True, blank=True,
    )
    ip_address = models.GenericIPAddressField()
    endpoint = models.CharField(max_length=255)
    status_code = models.IntegerField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_name = self.user.get_full_name() if self.user else 'Anonymous'
        return f"{user_name} - {self.endpoint} - {self.created_at}"
