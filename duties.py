from __future__ import annotations

import os
import pathlib
import re
import shutil

from duty import duty


PACKAGE_NAME = "panaetius"


@duty
def update_deps(ctx, dry: bool = False):
    """
    Update the dependencies using Poetry.

    Example:
        `duty update_deps dry=False`
    """
    dry_run = "--dry-run" if dry else ""
    ctx.run(
        ["poetry", "update", dry_run],
        title=f"Updating poetry deps {dry_run}",
    )


@duty
def test(ctx):
    """Run tests using pytest"""
    pytest_results = ctx.run(["pytest", "-v"])
    print(pytest_results)


@duty
def coverage(ctx):
    """
    Generate a coverage HTML report.

    Example:
        `duty coverage`
    """
    ctx.run(["coverage", "run", "--source", PACKAGE_NAME, "-m", "pytest"])
    ctx.run(["coverage", "html"])


@duty
def version(ctx, bump: str = "patch"):
    """
    Bump the version using Poetry and update _version.py.

    Args:
        bump (str, optional) = poetry version flag. Available options are:
            patch, minor, major, prepatch, preminor, premajor, prerelease.
            Defaults to patch.

    Example:
        `duty version bump=major`
    """

    # bump with poetry
    result = ctx.run(["poetry", "version", bump])
    new_version = re.search(r"(?:.*)(?:\s)(\d+\.\d+\.\d+)$", result)
    print(new_version.group(0))

    # update _version.py
    version_file = pathlib.Path(PACKAGE_NAME) / "_version.py"
    with version_file.open("w", encoding="utf-8") as version_file:
        version_file.write(
            f'"""Module containing the version of {PACKAGE_NAME}."""\n\n'
            + f'__version__ = "{new_version.group(1)}"\n'
        )
    print(f"Bumped _version.py to {new_version.group(1)}")


@duty
def build(ctx):
    """
    Build with poetry and extract the `setup.py` and copy to project root.

    Example:
        `duty build`
    """

    repo_root = pathlib.Path(".")

    # build with poetry
    result = ctx.run(["poetry", "build"])
    print(result)

    # extract the setup.py from the tar
    extracted_tar = re.search(r"(?:.*)(?:Built\s)(.*)", result)
    tar_file = pathlib.Path(f"./dist/{extracted_tar.group(1)}")
    shutil.unpack_archive(tar_file, tar_file.parents[0])

    # copy setup.py to repo root
    extracted_path = tar_file.parents[0] / os.path.splitext(tar_file.stem)[0]
    setup_py = extracted_path / "setup.py"
    shutil.copyfile(setup_py, (repo_root / "setup.py"))

    # cleanup
    shutil.rmtree(extracted_path)


@duty
def export(ctx):
    """
    Export the dependencies to a requirements.txt file.

    Example:
        `duty export`
    """
    requirements_content = ctx.run(
        [
            "poetry",
            "export",
            "-f",
            "requirements.txt",
            "--without-hashes",
        ]
    )
    requirements_dev_content = ctx.run(
        [
            "poetry",
            "export",
            "-f",
            "requirements.txt",
            "--without-hashes",
            "--dev",
        ]
    )

    requirements = pathlib.Path(".") / "requirements.txt"
    requirements_dev = pathlib.Path(".") / "requirements_dev.txt"

    with requirements.open("w", encoding="utf-8") as req:
        req.write(requirements_content)

    with requirements_dev.open("w", encoding="utf-8") as req:
        req.write(requirements_dev_content)
