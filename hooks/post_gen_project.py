#!/usr/bin/env python3
"""Post-generation hook for cookiecutter template."""

import subprocess
import sys


def run_command(cmd):
    """Run a shell command and return True if successful."""
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False


def main():
    """Initialize git repository with empty root commit."""
    print("Initializing git repository...")
    
    if not run_command("git init"):
        print("Failed to initialize git repository")
        sys.exit(1)
    
    if not run_command("git commit --allow-empty -m 'chore: initial empty root-commit'"):
        print("Failed to create initial empty commit")
        sys.exit(1)
    
    print("Adding project skeleton files...")
    
    if not run_command("git add ."):
        print("Failed to add files to git")
        sys.exit(1)
    
    if not run_command("git commit -m 'chore: add project skeleton'"):
        print("Failed to commit project skeleton")
        sys.exit(1)
    
    print("Git repository initialized with empty root commit and project skeleton")


if __name__ == "__main__":
    main()