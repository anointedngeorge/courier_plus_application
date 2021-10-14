from django.contrib.auth.models import Group

# the roles will be fetched using the group manager database

def group_to_roles():
    try:
        gp = []
        groups = Group.objects.all()
        for group in groups:
            if group.name == "superadmin":
                pass
            else:
                gp.append((group.name, group.name.upper()))
        return gp
    except:
        pass


