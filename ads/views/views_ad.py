from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Category, Selection
from ads.permissions import AdUpdateDeletePermission, SelectionChangePermission
from ads.serializers.ad import AdListSerializer, AdCreateSerializer, AdUpdateSerializer, AdDeleteSerializer, \
    CategorySerializer, SelectionSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer

    default_permission = [AllowAny()]
    permission_list = {
        "create": [IsAuthenticated(), SelectionChangePermission()],
        "retrieve": [AllowAny()],
        "update": [IsAuthenticated(), SelectionChangePermission()],
        "update_partial": [IsAuthenticated(), SelectionChangePermission()],
        "destroy": [IsAuthenticated(), SelectionChangePermission()]
    }

    def get_permissions(self):
        return self.permission_list.get(self.action, self.default_permission)


class AdListView(ListAPIView):
    queryset = Ad.objects.order_by("-price")
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        category_id = request.GET.get("cat", None)
        if category_id:
            self.queryset = self.queryset.filter(
                category_id=category_id
            )

        text = request.GET.get("text", None)
        if text:
            self.queryset = self.queryset.filter(
                name__icontains=text
            )

        locations = request.GET.getlist("location", None)
        locations_q = None
        for location in locations:
            if not locations_q:
                locations_q = Q(author__location__name__icontains=location)
            else:
                locations_q |= Q(author__location__name__icontains=location)
        if locations_q:
            self.queryset = self.queryset.filter(locations_q)

# Что-то я заморочился проверять параметры... Потом решил остановиться на обрезании слэша и обнуления пустоты
# На остальное DRF поругается)
        if 'price_from' in request.GET and 'price_to' in request.GET:
            price_from = request.GET.get("price_from")
            price_to = request.GET.get("price_to")
            if price_to[-1] == '/':
                price_to = price_to[:-1]
            if price_to == '':
                price_to = '0'
            if price_from == '':
                price_from = '0'

        # price_from = round(float(request.GET.get("price_from", 0)), 2)
        # price_to = round(float(request.GET.get("price_to", 0)), 2)
            self.queryset = self.queryset.filter(price__range=(price_from, price_to))

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, AdUpdateDeletePermission]


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDeleteSerializer
    permission_classes = [IsAuthenticated, AdUpdateDeletePermission]


@method_decorator(csrf_exempt, name='dispatch')
class AdImageUploadView(UpdateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({"name": self.object.name, "image": self.object.image.url})
