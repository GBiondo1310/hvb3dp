"""Tool created so I remember to update the projejct version everytime I commit"""

from pick import pick


def parse_version():
    with open("pyproject.toml", mode="r") as toml:
        lines = toml.readlines()
    return lines


def find_version_line(lines: list[str]) -> list[str, int]:
    for line in lines:
        if "version = " in line:
            return line


def get_version(line: str) -> str:
    return line.replace("version = ", "")


def increase_version(version: str, increase_type: int) -> str:
    """Increase type can be:
    - 0 -> Major release;
    - 1 -> Add feature;
    - 2 -> Bug fixes;
    - 3 -> Dev"""

    major, feature, bug, dev = version.replace('"', "").replace("\n", "").split(".")
    dev = dev.replace("dev", "")
    match increase_type:
        case 0:
            major = int(major) + 1
            feature = 0
            bug = 0
            dev = "dev0"

        case 1:
            feature = int(feature) + 1
            bug = 0
            dev = "dev0"

        case 2:
            bug = int(bug) + 1
            dev = "dev0"

        case 3:
            dev = "dev" + str(int(dev) + 1)

    return f'version = "{major}.{feature}.{bug}.{dev}"\n'


def substitute_version_line(version: str, lines: list[str]) -> list[str]:
    for i, line in enumerate(lines):
        if "version = " in line:
            lines[i] = version
            return lines


def write_back(lines: list[str]):
    with open("pyproject.toml", mode="w") as toml:
        toml.write("".join(lines))


def run():

    lines = parse_version()
    line = find_version_line(lines)
    version = get_version(line)

    options = ["Major release", "Add feature", "Bug fixes", "Dev"]

    _, index = pick(options, "Version increase type:", "->", 3)

    version = increase_version(version, index)

    substitute_version_line(version, lines)

    write_back(lines)


if __name__ == "__main__":
    run()
