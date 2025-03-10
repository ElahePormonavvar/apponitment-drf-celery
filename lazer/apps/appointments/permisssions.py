from rest_framework.permissions import BasePermission

# ----------------------------------------------------------------------------
class IsDoctorOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.doctor or request.user.is_staff
    
# ----------------------------------------------------------------------------
class RoleBasedPermission(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        return request.user.role in self.allowed_roles
    
# ----------------------------------------------------------------------------
class IsDoctor(RoleBasedPermission):
    allowed_roles = ['doctor']
# ----------------------------------------------------------------------------
class IsPatient(RoleBasedPermission):
    allowed_roles = ['patient']
# ----------------------------------------------------------------------------
class IsReceptionistOrDoctor(RoleBasedPermission):
    allowed_roles = ['receptionist', 'doctor']