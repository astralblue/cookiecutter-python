#!/usr/bin/env python3
"""Post-generation hook for cookiecutter template."""

import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path


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


def fetch_supported_python_versions():
    """Fetch currently supported Python versions from endoflife.date API."""
    try:
        # Fetch Python version data from endoflife.date API
        with urllib.request.urlopen("https://endoflife.date/api/python.json") as response:
            data = json.loads(response.read().decode())
        
        # Filter for Python 3.x versions that are still supported (not EOL)
        supported_versions = []
        for version_info in data:
            cycle = version_info.get("cycle", "")
            eol = version_info.get("eol", False)
            
            # Check if it's Python 3.x and not end-of-life
            if cycle.startswith("3.") and not eol:
                # Extract major.minor version
                match = re.match(r"3\.(\d+)", cycle)
                if match:
                    minor = int(match.group(1))
                    supported_versions.append(minor)
        
        # Sort versions and return unique values
        supported_versions = sorted(set(supported_versions))
        print(f"Fetched supported Python 3.x versions: {[f'3.{v}' for v in supported_versions]}")
        return supported_versions
        
    except Exception as e:
        print(f"Failed to fetch Python versions from endoflife.date API: {e}")
        # Don't use fallback - let caller handle the error
        return None


def parse_version_range(version_range):
    """Parse version range like '3.10-3.12', '3.10-', '-3.12', or '3.10'."""
    version_range = version_range.strip()
    
    # Handle single version case
    if "-" not in version_range:
        match = re.match(r"3\.(\d+)", version_range)
        if match:
            version = int(match.group(1))
            return version, version
        else:
            return None, None
    
    # Split on dash
    parts = version_range.split("-", 1)
    min_version = None
    max_version = None
    
    # Parse minimum version
    if parts[0].strip():
        match = re.match(r"3\.(\d+)", parts[0].strip())
        if match:
            min_version = int(match.group(1))
    
    # Parse maximum version
    if len(parts) > 1 and parts[1].strip():
        match = re.match(r"3\.(\d+)", parts[1].strip())  
        if match:
            max_version = int(match.group(1))
    
    return min_version, max_version


def generate_python_metadata():
    """Generate Python version metadata based on version range."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("pyproject.toml not found, skipping metadata generation")
        return
    
    # Read pyproject.toml
    content = pyproject_path.read_text()
    
    # Extract python_version_range
    match = re.search(r'requires-python\s*=\s*"([^"]+)"', content)
    if not match:
        print("Could not find requires-python in pyproject.toml")
        return
    
    version_range = match.group(1)
    print(f"Found python_version_range: {version_range}")
    
    # Parse the version range first
    min_version, max_version = parse_version_range(version_range)
    
    # Check if we need to fetch from internet
    need_internet = min_version is None or max_version is None
    
    if need_internet:
        print("Version range requires internet lookup for defaults...")
        supported_versions = fetch_supported_python_versions()
        if supported_versions is None:
            print()
            print("ERROR: Cannot generate Python version metadata.")
            print(f"The version range '{version_range}' requires fetching current Python")
            print("support information from the internet, but the request failed.")
            print()
            print("Solutions:")
            print("1. Check your internet connection and try again")
            print("2. Specify both min and max versions explicitly (e.g., '3.10-3.13')")
            print("   to avoid needing internet access")
            print()
            sys.exit(1)
        
        # Apply defaults if min/max not specified
        if min_version is None:
            min_version = min(supported_versions)
            print(f"No minimum version specified, using oldest supported: 3.{min_version}")
        
        if max_version is None:
            max_version = max(supported_versions)
            print(f"No maximum version specified, using newest supported: 3.{max_version}")
        
        # Filter supported versions to the specified range
        target_versions = [v for v in supported_versions if min_version <= v <= max_version]
    else:
        print("Both min and max versions specified, skipping internet lookup")
        # Generate target versions from the specified range
        target_versions = list(range(min_version, max_version + 1))
    
    if not target_versions:
        print(f"No versions found in range 3.{min_version}-3.{max_version}")
        return
    
    print(f"Target Python versions: {[f'3.{v}' for v in target_versions]}")
    
    # Generate requires-python field
    requires_python = f">=3.{min_version}"
    
    # Generate classifiers
    classifiers = ['"Programming Language :: Python :: 3"']
    for version in target_versions:
        classifiers.append(f'"Programming Language :: Python :: 3.{version}"')
    
    # Create the classifiers section
    classifiers_text = ",\n    ".join(classifiers)
    
    # Replace requires-python
    new_content = re.sub(
        r'requires-python\s*=\s*"[^"]+"',
        f'requires-python = "{requires_python}"',
        content
    )
    
    # Replace the Python 3 classifier with all generated classifiers
    pattern = r'"Programming Language :: Python :: 3",'
    replacement = classifiers_text + ","
    new_content = re.sub(pattern, replacement, new_content)
    
    # Write back to file
    pyproject_path.write_text(new_content)
    print(f"Updated requires-python: {requires_python}")
    print(f"Updated Python version classifiers: {[f'3.{v}' for v in target_versions]}")


def main():
    """Initialize git repository with empty root commit and update metadata."""
    print("Generating dynamic Python version metadata...")
    generate_python_metadata()
    
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