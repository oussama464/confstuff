from dataclasses import dataclass
import shlex


@dataclass
class Command:
    command: str
    args: list[str]

def run_command(command:str) ->None:
    match command:
        case "quit":
            print("Goodbye")
            quit()
        case "reset":
            print("Reset")
        case _:
            print(f"Unknown command")

def run_command_v2(command:str) ->None:
    match command.split():
        case ("load",filename):
            print(f"Loading {filename=}")
        case ("save",filename):
            print(f"Saving {filename=}")

        case ("quit" | "exit"| "bye",*rest) if "--force" in rest or "-f" in rest:
            print("Force quitting")
            quit()

        case ("quit" | "exit" | "bye", *rest):
            print("Goodbye")
            quit()

        case _:
            print(f"Unknown command")


def run_command_v3(command:Command) ->None:
    match command:
        case Command("load",args=[filename]):
            print(f"Loading {filename=}")

        case Command("save",[filename]):
            print(f"Saving {filename=}")

        case Command("quit" | "exit"| "bye",args=['-f' | '--force',*rest]):
            print("Force quitting")
            quit()

        case Command("quit" | "exit" | "bye"):
            print("Goodbye")
            quit()

        case _:
            print(f"Unknown command")
def main() -> None:
    while True:
        command,*arguments = shlex.split(input("$ "))
        run_command_v3(Command(command,arguments))

if __name__ == "__main__":
    main()
