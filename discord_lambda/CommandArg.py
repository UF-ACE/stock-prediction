class CommandArg:
    class Choice:
        def __init__(self, name: str, value: str = None) -> None:
            self.name = name
            self.value = value if value else name

        def to_dict(self) -> dict:
            return {
                "name": self.name,
                "value": self.value
            }


    class Types:
        STRING = 3
        INTEGER = 4
        BOOLEAN = 5
        USER = 6
        CHANNEL = 7
        ROLE = 8
        MENTIONABLE = 9
        NUMBER = 10
        ATTACHMENT = 11
        

    def __init__(self, name: str, desc: str, type: int, required: bool = True, choices: list[Choice] = None) -> None:
        self.name = name
        self.desc = desc
        self.required = required
        self.choices = choices
        self.type = type

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.desc,
            "type": self.type,
            "required": self.required,
            "choices": [choice.to_dict() for choice in self.choices] if self.choices else None
        }   