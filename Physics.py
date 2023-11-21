class Physics:

    @staticmethod
    def collide(obj1, obj2):
        offset_x = int(obj1.position.x - obj2.position.x) * 32
        offset_y = int(obj1.position.y - obj2.position.y) * 32
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

    @staticmethod
    def outOfScreen(hitbox, width, height):
        return hitbox.x > width or hitbox.x + (hitbox.w//2) < 0 or hitbox.y > height or hitbox.y + (hitbox.h // 2) < 0

    @staticmethod
    def hitboxes_collide(hitbox1, hitbox2):
        return hitbox1.colliderect(hitbox2)
