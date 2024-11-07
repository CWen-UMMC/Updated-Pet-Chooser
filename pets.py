class Pets:
    def __init__(self, pet_id, name, species, age, owner):
        self.pet_id = pet_id
        self.name = name
        self.species = species
        self.age = age
        self.owner = owner

    def __str__(self):
        return f"{self.name}, the {self.species}. {self.name} is {self.age} years old. {self.name}'s owner is {self.owner}."
