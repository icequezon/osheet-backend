from database import db
from .models import Floor, FloorImage, FloorLinen, LinenType

class FloorService():
    @staticmethod
    def create(name):
        floor = Floor()
        floor.name = name
        db.session.add(floor)
        db.session.commit()

    @staticmethod
    def get_all_floors():
        return Floor.query.all();

    @staticmethod
    def get(id):
        floor = Floor.query.filter_by(id=id).first()
        if not floor:
            raise Exception("Floor not found")

        return floor

    @staticmethod
    def update_image(id, image, timestamp):
        floor = Floor.query.filter_by(id=id).first()
        if not floor:
            raise Exception("Floor not found")
        floor_image = FloorImage()
        floor_image.image = image
        floor_image.timestamp = timestamp
        db.session.add(floor_image)
        db.session.commit()
        floor.latest_image_id = floor_image.id
        db.session.commit()

        return floor

    @staticmethod
    def delete(id):
        Floor.query.filter_by(id=id).delete()
        db.session.commit()

    @staticmethod
    def add_linen(id, linen_type_id):
        floor = Floor.query.filter_by(id=id).first()
        if not floor:
            raise Exception("Floor not found")
        floor_linen = FloorLinen()
        floor_linen.ltype_id = linen_type_id;
        floor_linen.floor_id = id;
        floor_linen.quantity = 0;
        db.session.add(floor_linen)
        db.session.commit()

class LinenTypeService():
    @staticmethod
    def create(name):
        linen_type = LinenType()
        linen_type.name = name
        db.session.add(linen_type)
        db.session.commit()

    @staticmethod
    def get_all_linen_types():
        return LinenType.query.all();

    @staticmethod
    def get(id):
        linen_type = LinenType.query.filter_by(id=id).first()
        if not linen_type:
            raise Exception("LinenType not found")

        return linen_type

    @staticmethod
    def delete(id):
        LinenType.query.filter_by(id=id).delete()
        db.session.commit()
