class Serializer():
    fields = []
    def serialize(self, item):
        if item is None:
            return {}

        serialized_item = {}
        for field in self.fields:
            if isinstance(field, tuple):
                serialized_item[field[1]] = getattr(item, field[0])
                continue
            serialized_item[field] = getattr(item, field)

        return serialized_item

    def serializeMany(self, items):
        return [ self.serialize(item) for item in items ]

class FloorImageSerializer(Serializer):
    fields = ['id', 'image', 'timestamp']

class LinenTypeSerializer(Serializer):
    fields = ['id', 'name']

class LinenSerializer(Serializer):
    def serialize(self, item):
        return {
            'id': item.id,
            'type': item.ltype.name,
            'quantity': item.quantity
        }

class FloorSerializer(Serializer):
    def serialize(self, item):
        latest_image = FloorImageSerializer().serialize(item.latest_image)
        linens = LinenSerializer().serializeMany(item.floor_linen)
        return {
            'id': item.id,
            'name': item.name,
            'latestImage': latest_image,
            'hasTrolley': item.has_trolley,
            'linens': linens,
        }
