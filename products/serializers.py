from rest_framework import serializers


class ProductImageSerializer(serializers.Serializer):
    public_id = serializers.CharField(required=True)
    url = serializers.URLField(required=True)


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    category = serializers.CharField(required=True)
    material = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    colors = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
    )
    weight = serializers.FloatField(required=False, allow_null=True)
    dimensions = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    supplier = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    price = serializers.FloatField(required=True)
    stock = serializers.IntegerField(required=False, default=0)
    images = ProductImageSerializer(many=True, required=False, default=list)


class ProductSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    sku = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, allow_null=True)
    category = serializers.CharField()
    material = serializers.CharField(allow_blank=True, allow_null=True)
    colors = serializers.ListField(child=serializers.CharField())
    weight = serializers.FloatField(allow_null=True)
    dimensions = serializers.CharField(allow_blank=True, allow_null=True)
    supplier = serializers.CharField(allow_blank=True, allow_null=True)
    status = serializers.CharField()
    price = serializers.FloatField()
    stock = serializers.IntegerField()
    images = ProductImageSerializer(many=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_id(self, product):
        return str(product.id)
