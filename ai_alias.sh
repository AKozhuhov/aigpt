#!/bin/bash

# Check if the alias already exists in the ~/.bash_profile
if ! grep -q "alias ai=" "$HOME/.bash_profile"; then
  # Add the alias to the ~/.bash_profile
  echo "alias ai='python3 \$PWD/main.py'" >> "$HOME/.bash_profile"
  echo "Alias 'ai' added successfully."
else
  echo "Alias 'ai' already exists."
fi

# Source the updated ~/.bash_profile
source "$HOME/.bash_profile"
