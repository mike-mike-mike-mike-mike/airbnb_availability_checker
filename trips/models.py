from django.db import models
from django.contrib.auth.models import User


class Trip(models.Model):
    room_id = models.CharField(max_length=64)
    check_in = models.DateField()
    check_out = models.DateField()
    available = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def trip_id(self):
        return f"{self.room_id}_{self.check_in}_{self.check_out}"

    def __str__(self):
        fields = [
            f"{field.name}: {getattr(self, field.name)}" for field in self._meta.fields
        ]
        return f"{self.__class__.__name__}({', '.join(fields)})"


class RoomDetail(models.Model):
    room_id = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        display_name = (
            f"{self.display_name[:32]}"
            f"{'' if len(self.display_name) <= 32 else '...'}"
        )
        return f"{self.__class__.__name__}(room_id: {self.room_id}, display_name: {display_name})"
