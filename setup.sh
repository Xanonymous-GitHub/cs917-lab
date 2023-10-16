#!/usr/bin/env bash

# Set the script to fail if any command fails.
set -euo pipefail

function setup() {
  # Set target python version from the .python-version file.
  local PYTHON_VERSION
  PYTHON_VERSION=$(cat .python-version)

  # Check if target python version has been installed by pyenv. If not, install it.
  if ! pyenv versions | grep -q "$PYTHON_VERSION"; then
      pyenv install "$PYTHON_VERSION"
  fi

  # Update poetry itself.
  poetry self update

  # Set local python version to the target version.
  pyenv local "$PYTHON_VERSION"

  # Set poetry virtualenv to the target version.
  poetry env use "$PYTHON_VERSION"

  # Install dependencies.
  poetry install
}

setup && echo "Setup complete. Now run 'poetry shell' to activate the virtualenv."
