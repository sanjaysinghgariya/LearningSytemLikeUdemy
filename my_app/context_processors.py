from my_app.models import Categories


def footer(request):
    category = Categories.objects.all()
    return {'category': category}