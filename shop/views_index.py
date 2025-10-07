from django.http import JsonResponse

def api_index(request):
    return JsonResponse({
        "endpoints": {
            "authors": "/authors",
            "author_detail": "/authors/{id}",
            "colorings": "/colorings",
            "coloring_detail": "/colorings/{id}",
            "pencils": "/pencils",
            "pencil_detail": "/pencils/{id}"
        },
        "note": "No trailing slash."
    })
