from django.contrib import admin
from schedule.models import TakuModel, UserModel, TakuDate, TakuMember, TakuSuke, PersonalSchedule

@admin.register(TakuModel)
class TakuModel(admin.ModelAdmin):
    pass

admin.site.register(UserModel)
admin.site.register(TakuDate)
admin.site.register(TakuMember)
admin.site.register(TakuSuke)
admin.site.register(PersonalSchedule)