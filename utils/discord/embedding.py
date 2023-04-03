class Embedding:
    def __init__(self, title: str = "", description: str = "", url: str = "", color: int = "", fields: list = [], footer: dict = {}):
        self.title = title
        self.description = description
        self.url = url
        self.color = color
        self.fields = fields
        self.footer = footer
    
    def to_dict(self):
        return {
            "title": self.title if self.title else None,
            "description": self.description if self.description else None,
            "url": self.url if self.url else None,
            "color": self.color if self.color else None,
            "fields": self.fields if self.fields else None,
            "footer": self.footer if self.footer else None
        }
    
    def set_title(self, title: str):
        self.title = title
    
    def set_description(self, description: str):
        self.description = description

    def set_url(self, url: str):
        self.url = url
    
    def set_color(self, color: int):
        self.color = color
    
    def add_field(self, name: str, value: str, inline: bool):
        self.fields.append({"name": name, "value": value, "inline": inline})
    
    def set_footer(self, text: str, icon_url: str = "https://uf-ace.com/static/media/logo-min.1380c5e0.png"):
        self.footer = {"text": text, "icon_url": icon_url}