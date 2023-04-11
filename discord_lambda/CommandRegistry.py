import os
import importlib
import requests
from .CommandArg import CommandArg


def prune_registry(d: dict) -> dict:
        if isinstance(d, dict):
            return {k: prune_registry(v) if k != "func" else None for k, v in d.items()}
        elif isinstance(d, list):
            return [prune_registry(item) for item in d]
        else:
            return d


class CommandRegistry:
    def __init__(self, command_dir: str, app_id: str, bot_token: str) -> None:
        self.commands = {}
        self.__register_commands(command_dir)
        self.__update_commands(app_id, bot_token)

        
    def __register_commands(self, command_dir: str) -> None:
        # Load all the commands from the command directory
        for file in os.listdir(command_dir):
            if file.endswith('.py'):
                try:
                    module = importlib.import_module(command_dir.replace('/', '.') + '.' + file[:-3])
                    met = getattr(module, 'setup')
                except Exception as e:
                    raise Exception(f"Unable to load command '{file}': {e}")
                else:
                    met(self)
                    print(f"Loaded command '{file}'")


    def __update_commands(self, app_id: str, bot_token: str) -> None:
        # Update the application commands with the Discord API
        cmd_list = prune_registry(self.commands)
        cmd_list = list(cmd_list.values())

        url = f"https://discord.com/api/v10/applications/{app_id}/commands"
        headers = {
            "Authorization": f"Bot {bot_token}"
        }
        try:
            requests.put(url, json=cmd_list, headers=headers).raise_for_status()
        except Exception as e:
            raise Exception(f"Unable to update application commands: {e}")
        

    def register_cmd_group(self, name: str, desc: str = None, parent_group: str = None) -> None:
        if not parent_group:   # Registering a top-level command group
            self.commands[name] = self.commands.get(name, {})
            self.commands[name] = {
                "name": name,
                "description": desc,
                "options": []
            }

        else:    # Registering a subcommand group
            try:
                self.commands[parent_group][name] = {
                    "name": name,
                    "description": desc,
                    "type": 2,
                    "options": []
                }
            except KeyError:
                raise KeyError(f"Parent command group '{parent_group}' does not exist!")

    
    def register_cmd(self, func: callable, name: str, desc: str = None, cmd_group: str = None, sub_cmd_group: str = None, options: list[CommandArg] = None) -> None:
        if sub_cmd_group and not cmd_group:
            raise Exception("Subcommand groups must be registered under a parent command group!")
        
        if cmd_group:
            if sub_cmd_group:
                self.commands[cmd_group][sub_cmd_group]["options"].append({
                    "name": name,
                    "description": desc,
                    "type": 1,
                    "options": [opt.to_dict() for opt in options],
                    "func": func
                })
            else:
                self.commands[cmd_group]["options"].append({
                    "name": name,
                    "description": desc,
                    "type": 1,
                    "options": [opt.to_dict() for opt in options],
                    "func": func
                })
        
        else:
            self.commands[name] = {
                "name": name,
                "description": desc,
                "type": 1,
                "options": [opt.to_dict() for opt in options],
                "func": func
            }
    

    def find_func(self, d: dict) -> tuple[callable, dict]:
        try:
            cmd = self.commands[d["name"]]
            while cmd.get("type", 0) != 1:
                d = d["options"][0]
                cmd = cmd[d["name"]]
        except KeyError:
            raise KeyError(f"Command '{d['name']}' not found!")
        
        func = cmd.get("func")
        try:
            assert callable(func)
        except AssertionError:
            raise AssertionError(f"Command '{d['name']}' is not callable!")
        
        # Check if any arguments were passed
        if not d.get("options"):
            return func, {}
        else:
            return func, {option["name"]: option["value"] for option in d["options"]}