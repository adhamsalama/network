from django.core.paginator import Paginator


def paginate(posts, page_number=1):
    paginator = Paginator(posts, 10)
    # pages start at 0, less than zero or more than max page number gives the last page
    page_obj = paginator.get_page(page_number)
    return {"paginator": paginator, "page_obj": page_obj, "posts": page_obj.object_list}
