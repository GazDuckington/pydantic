import dataclasses, random, string
from dataclasses import dataclass, field

def generate_id() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=12))

def get_random(a, b) -> str:
    return "".join(random.choices(a+string.digits, k=b))

# slots can't be used in multi-inheritance scenario
# by default dataclass uses __dict__, but slots are faster
@dataclass(order=True, frozen=True, kw_only=True, slots=True)
class Person:
    sort_index: int = field(init=False, repr=False)
    id: str = field(init=False, default_factory=generate_id)
    name: str
    job: str
    age: int
    strength: int = 100
    _search_string: str = field(init=False, repr=False)
    _random: str = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, 'sort_index', self.strength)
        object.__setattr__(self, '_random', get_random(self.name, self.age))
        # self.search_string = f"{self.job} {self.strength}"
        object.__setattr__(self, "_search_string", f"{self.job} {self.strength}")
    
    # def __str__(self):
    #     return f'{self.name}, {self.age}, {self.job}'

def main() -> None:
    person1 = Person(name="Geralt", job="Witcher", age=37, strength=77)
    person2 = Person(name="Yennefer", job="Sorcerer", age=30, strength=89)
    person3 = Person(name="Dandelion", job="bard", age=40, strength=20)

    print(person2)
    # print(person1<person3)
    # print(Person.__annotations__)
    # print(dataclasses.fields(Person))

if __name__ == "__main__":
    main()