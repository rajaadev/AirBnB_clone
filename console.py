#!/usr/bin/python3
"""Module entry point of the command interpreter."""

import cmd
import re
import json
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """Class command interpreter."""

    prompt = "(hbnb) "

    def default(self, line):
        """Catch commands if nothing else matches then."""
        self._precmd(line)

    def _precmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        match = re.search(r"^(\w+)\.(\w+)\(([^)]*)\)$", line)
        if match:
            classname, method, args = match.groups()
            match_uid_and_args = re.search(r'^"([^"]*)"(?:, (.*))?$', args)
            uid, attr_or_dict = (match_uid_and_args.groups() if match_uid_and_args else (args, None))

            if method == "update" and attr_or_dict:
                match_dict = re.search(r'^({.*})$', attr_or_dict)
                if match_dict:
                    self.update_dict(classname, uid, match_dict.group(1))
                    return ""
                match_attr_and_value = re.search(r'^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
                if match_attr_and_value:
                    attr_and_value = (match_attr_and_value.group(1) or "") + " " + (match_attr_and_value.group(2) or "")
            else:
                attr_and_value = ""
            command = f"{method} {classname} {uid} {attr_and_value}"
            self.onecmd(command)
            return command
        return line

    def update_dict(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        try:
            data = json.loads(s_dict.replace("'", '"'))
        except json.JSONDecodeError:
            print("** invalid dictionary format **")
            return

        if not classname:
            print("** class name missing **")
            return
        if classname not in storage.classes():
            print("** class doesn't exist **")
            return
        if not uid:
            print("** instance id missing **")
            return

        key = f"{classname}.{uid}"
        if key not in storage.all():
            print("** no instance found **")
            return

        obj = storage.all()[key]
        attributes = storage.attributes()[classname]
        for attr, value in data.items():
            if attr in attributes:
                value = attributes[attr](value)
            setattr(obj, attr, value)
        obj.save()

    def do_EOF(self, line):
        """Handles End Of File character."""
        print()
        return True

    def do_quit(self, line):
        """Exits the program."""
        return True

    def emptyline(self):
        """Doesn't do anything on ENTER."""
        pass

    def do_create(self, line):
        """Creates an instance."""
        if not line:
            print("** class name missing **")
            return
        if line not in storage.classes():
            print("** class doesn't exist **")
            return
        instance = storage.classes()[line]()
        instance.save()
        print(instance.id)

    def do_show(self, line):
        """Prints the string representation of an instance."""
        if not line:
            print("** class name missing **")
            return
        words = line.split()
        if len(words) < 1:
            print("** class name missing **")
            return
        if words[0] not in storage.classes():
            print("** class doesn't exist **")
            return
        if len(words) < 2:
            print("** instance id missing **")
            return
        key = f"{words[0]}.{words[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id."""
        if not line:
            print("** class name missing **")
            return
        words = line.split()
        if len(words) < 1:
            print("** class name missing **")
            return
        if words[0] not in storage.classes():
            print("** class doesn't exist **")
            return
        if len(words) < 2:
            print("** instance id missing **")
            return
        key = f"{words[0]}.{words[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances."""
        if line:
            words = line.split()
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
                return
            nl = [str(obj) for key, obj in storage.all().items() if type(obj).__name__ == words[0]]
            print(nl)
        else:
            print([str(obj) for key, obj in storage.all().items()])

    def do_count(self, line):
        """Counts the instances of a class."""
        if not line:
            print("** class name missing **")
            return
        words = line.split()
        if words[0] not in storage.classes():
            print("** class doesn't exist **")
            return
        print(len([key for key in storage.all() if key.startswith(f"{words[0]}.")]))

    def do_update(self, line):
        """Updates an instance by adding or updating attribute."""
        if not line:
            print("** class name missing **")
            return

        match = re.search(r'^(\S+)\s(\S+)(?:\s(\S+)(?:\s(.*))?)?', line)
        if not match:
            print("** class name missing **")
            return

        classname, uid, attribute, value = match.groups()
        if not classname:
            print("** class name missing **")
            return
        if classname not in storage.classes():
            print("** class doesn't exist **")
            return
        if not uid:
            print("** instance id missing **")
            return

        key = f"{classname}.{uid}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if not attribute:
            print("** attribute name missing **")
            return
        if not value:
            print("** value missing **")
            return

        value = value.strip('"')
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass

        obj = storage.all()[key]
        setattr(obj, attribute, value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
