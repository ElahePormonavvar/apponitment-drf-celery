from rest_framework import permissions



# فقط دکتر نوبت یا کاربران staff می‌توانند حذف کنند
class IsDoctorOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.doctor or request.user.is_staff