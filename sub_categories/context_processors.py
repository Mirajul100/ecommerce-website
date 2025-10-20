from sub_categories.models import SubCategory

def sub_menu_links (request):
    sub_link = SubCategory.objects.all()
    return dict(sub_link=sub_link)