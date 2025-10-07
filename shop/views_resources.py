from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Coloring, Pencil
from .serializers import AuthorSerializer, ColoringSerializer, PencilSerializer

def paginate(request, qs):
    page = int(request.query_params.get("page", 1))
    limit = int(request.query_params.get("limit", 20))
    start, end = (page-1)*limit, (page-1)*limit + limit
    return qs[start:end], {"page": page, "limit": limit, "total": qs.count()}


class AuthorsListCreateAPIView(APIView):
    def get(self, request):
        qs = Author.objects.all().order_by("id")
        s = request.query_params.get("search")
        if s: qs = qs.filter(Q(name__icontains=s) | Q(bio__icontains=s))
        page_qs, meta = paginate(request, qs)
        return Response({"data": AuthorSerializer(page_qs, many=True).data, "meta": meta}, status=200)
    def post(self, request):
        ser = AuthorSerializer(data=request.data)
        if ser.is_valid():
            obj = ser.save()
            return Response(AuthorSerializer(obj).data, status=201)
        return Response({"error":{"code":"UnprocessableEntity","message":ser.errors}}, status=422)

class AuthorDetailAPIView(APIView):
    def get_obj(self, pk):
        try: return Author.objects.get(pk=pk)
        except Author.DoesNotExist: return None
    def get(self, request, pk):
        obj = self.get_obj(pk)
        if not obj: return Response({"error":{"code":"NotFound","message":"Author not found."}}, status=404)
        return Response(AuthorSerializer(obj).data, status=200)
    def put(self, request, pk):
        obj = self.get_obj(pk)
        if not obj: return Response({"error":{"code":"NotFound","message":"Author not found."}}, status=404)
        ser = AuthorSerializer(obj, data=request.data, partial=False)
        if ser.is_valid():
            obj = ser.save()
            return Response(AuthorSerializer(obj).data, status=200)
        return Response({"error":{"code":"UnprocessableEntity","message":ser.errors}}, status=422)
    def delete(self, request, pk):
        obj = self.get_obj(pk)
        if not obj: return Response({"error":{"code":"NotFound","message":"Author not found."}}, status=404)
        if obj.colorings.exists():
            return Response({"error":{"code":"Conflict","message":"Cannot delete author with existing colorings."}}, status=409)
        obj.delete()
        return Response(status=204)

class ColoringsListCreateAPIView(APIView):
    # GET /colorings?search=&author=&theme=&sort=price:asc|price:desc|title&page=&limit=
    def get(self, request):
        qs = Coloring.objects.select_related("author").all()
        search = request.query_params.get("search")
        author = request.query_params.get("author")
        theme = request.query_params.get("theme")
        sort = request.query_params.get("sort")
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(sku__icontains=search))
        if author:
            qs = qs.filter(author_id=author)
        if theme:
            qs = qs.filter(theme__iexact=theme)
        if sort == "title": qs = qs.order_by("title")
        elif sort == "price:asc": qs = qs.order_by("price")
        elif sort == "price:desc": qs = qs.order_by("-price")
        else: qs = qs.order_by("id")
        page_qs, meta = paginate(request, qs)
        return Response({"data": ColoringSerializer(page_qs, many=True).data, "meta": meta}, status=200)
    def post(self, request):
        ser = ColoringSerializer(data=request.data)
        if ser.is_valid():
            if ser.validated_data["price"] <= 0:
                return Response({"error":{"code":"UnprocessableEntity","message":"Price must be > 0."}}, status=422)
            obj = ser.save()
            return Response(ColoringSerializer(obj).data, status=201)
        return Response({"error":{"code":"UnprocessableEntity","message":ser.errors}}, status=422)

class ColoringDetailAPIView(APIView):
    def get_obj(self, pk):
        try: return Coloring.objects.get(pk=pk)
        except Coloring.DoesNotExist: return None
    def get(self, request, pk):
        obj = self.get_obj(pk)
        if not obj: return Response({"error":{"code":"NotFound","message":"Coloring not found."}}, status=404)
        return Response(ColoringSerializer(obj).data, status=200)
    def put(self, request, pk):
        obj = self.get_obj(pk)
        if not obj: return Response({"error":{"code":"NotFound","message":"Coloring not found."}}, status=404)
        ser = ColoringSerializer(obj, data=request.data, partial=False)
        if ser.is_valid():
            if ser.validated_data["price"] <= 0:
                return Response({"error":{"code":"UnprocessableEntity","message":"Price must be > 0."}}, status=422)
            obj = ser.save()
            return Response(ColoringSerializer(obj).data, status=200)
        return Response({"error":{"code":"UnprocessableEntity","message":ser.errors}}, status=422)
    def delete(self, request, pk):
        obj = self.get_obj(pk)
        if not obj: return Response({"error":{"code":"NotFound","message":"Coloring not found."}}, status=404)
        obj.delete()
        return Response(status=204)

class PencilsListCreateAPIView(APIView):
    # GET /pencils?search=&brand=&hardness=&sort=price:asc|price:desc|name&page=&limit=
    def get(self, request):
        qs = Pencil.objects.all()
        search = request.query_params.get("search")
        brand = request.query_params.get("brand")
        hardness = request.query_params.get("hardness")
        sort = request.query_params.get("sort")
        if search: qs = qs.filter(Q(name__icontains=search) | Q(sku__icontains=search))
        if brand: qs = qs.filter(brand__iexact=brand)
        if hardness: qs = qs.filter(hardness__iexact=hardness)
        if sort == "name": qs = qs.order_by("name")
        elif sort == "price:asc": qs = qs.order_by("price")
        elif sort == "price:desc": qs = qs.order_by("-price")
        else: qs = qs.order_by("id")
        page_qs, meta = paginate(request, qs)
        return Response({"data": PencilSerializer(page_qs, many=True).data, "meta": meta}, status=200)
    def post(self, request):
        ser = PencilSerializer(data=request.data)
        if ser.is_valid():
            if ser.validated_data["price"] <= 0:
                return Response({"error":{"code":"UnprocessableEntity","message":"Price must be > 0."}}, status=422)
            obj = ser.save()
            return Response(PencilSerializer(obj).data, status=201)
        return Response({"error":{"code":"UnprocessableEntity","message":ser.errors}}, status=422)

class PencilDetailAPIView(APIView):
    def get_obj(self, pk):
        try: return Pencil.objects.get(pk=pk)
        except Pencil.DoesNotExist: return None
    def get(self, request, pk):
        obj = self.get_obj(pk)
        if not obj: return Response({"error":{"code":"NotFound","message":"Pencil not found."}}, status=404)
        return Response(PencilSerializer(obj).data, status=200)
    def put(self, request, pk):
        obj = self.get_obj(pk)
        if not obj: return Response({"error":{"code":"NotFound","message":"Pencil not found."}}, status=404)
        ser = PencilSerializer(obj, data=request.data, partial=False)
        if ser.is_valid():
            if ser.validated_data["price"] <= 0:
                return Response({"error":{"code":"UnprocessableEntity","message":"Price must be > 0."}}, status=422)
            obj = ser.save()
            return Response(PencilSerializer(obj).data, status=200)
        return Response({"error":{"code":"UnprocessableEntity","message":ser.errors}}, status=422)
    def delete(self, request, pk):
        obj = self.get_obj(pk)
        if not obj: return Response({"error":{"code":"NotFound","message":"Pencil not found."}}, status=404)
        obj.delete()
        return Response(status=204)
