import platform
from os import system, chdir
from pick import pick
from tests.test import suite, runner, tests
from increase_proj_version import run as increase_version

if __name__ == "__main__":

    if platform.system() == "Windows":
        raise NotImplementedError("Commit.py does not work on windows")

    _, commit_if_test_not_passed = pick(
        [
            "DON'T COMMIT (Recommended)",
            "Commit anyway",
            "Don't run tests (Not recommended)",
        ],
        "Choose tests handling:",
    )

    _, generate_documentation_before_committing = pick(
        ["Generate", "Don't generate"], "Wether to generate documentation or not:"
    )

    _, push_to_origin = pick(
        ["Push to GitHub", "Don't push to GitHub"],
        "Wether to push this commit to GitHub or not:",
    )

    match commit_if_test_not_passed:

        case 0:
            tests_to_do = pick(tests, "Choos what you want to test:", "->", 0, True)
            result = runner.run(suite(*tests_to_do))
            if not result.wasSuccessful():
                print("Tests were not successful, commit aborted!")
                system("rm database.sqlite")
                quit()
            else:
                system("rm database.sqlite")

        case 1:
            tests_to_do = pick(tests, "Choos what you want to test:", "->", 0, True)
            result = runner.run(suite(*tests_to_do))
            system("rm database.sqlite")

        case 3:
            pass

    if generate_documentation_before_committing == 0:
        print("Generating documentation")
        chdir("hvb3dp")
        system("sphinx-apidoc -o ../docs .")
        chdir("../docs")
        system("sphinx-build -M html . _build")
        chdir("..")

    message = input("Commit message: ")
    increase_version()

    system("git add .")
    system(f'git commit -m "{message} - $(date)"')

    if push_to_origin == 0:
        system("git branch>branches")
        with open("branches", mode="r") as branches:
            lines = branches.readlines()

        for line in lines:
            if "*" in line:
                branch = line.replace("* ", "").replace(" ", "")
        system("rm branches")
        system(f"git push origin {branch}")
