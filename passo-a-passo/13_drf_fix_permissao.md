# Django Experience #13 - DRF: Fix Permissão


Doc: https://www.django-rest-framework.org/api-guide/permissions/


```python
#movie/viewsets.py
class CensurePermission(BasePermission):
    age_user = 14
    group_name = 'Infantil'
    message = 'Este filme não é permitido para este perfil.'

    def has_object_permission(self, request, view, obj):
        groups = request.user.groups.values_list('name', flat=True)

        censure = obj.censure

        if self.group_name in groups and censure >= self.age_user:
            response = {
                'message': self.message,
                'status_code': status.HTTP_403_FORBIDDEN
            }
            raise DRFValidationError(response)
        else:
            return True


class MovieViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = (DjangoModelPermissions, CensurePermission)
```
