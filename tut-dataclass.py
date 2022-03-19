from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Person:
    sort_index: int = field(init=False, repr=False)
    name: str
    job: str
    age: int
    strength: int = 100

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.strength)
    
    def __str__(self):
        return f'{self.name}, {self.age}, {self.job}'

def main() -> None:
    person1 = Person("Geralt", "Witcher", 37, 77)
    person2 = Person("Yennefer", "Sorcerer", 30, 89)
    person3 = Person("Dandelion", "bard", 40, 20)

    print(person2)
    print(person1<person3)

if __name__ == "__main__":
    main()