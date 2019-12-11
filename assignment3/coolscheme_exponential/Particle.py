class Particle():
    """ Each particle contains it's coordinates and has an ID. """

    def __init__(self, id, coordx, coordy):
        self.id = id
        self.x = coordx
        self.y = coordy

    def __str__(self):
        return f"Hi I am particle {self.id} at ({self.x}, {self.y})"