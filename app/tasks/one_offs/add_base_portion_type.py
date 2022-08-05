def add_base_portion_type():
    from app.models import User, PortionType

    for user in User.load_all():
        PortionType(name="základní", size=1, created_by=user.id).save()
