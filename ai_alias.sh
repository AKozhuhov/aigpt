#!/bin/bash

# Check if the "ai" alias already exists in the ~/.bash_profile
if ! grep -q "alias ai=" "$HOME/.bash_profile"; then
  # Add the "ai" alias to the ~/.bash_profile
  dir="$(pwd)"
  # Create the alias, linking it to the main.py script in the current directory using Python3
  echo "alias ai='python3 $dir/main.py'" >> "$HOME/.bash_profile"
  # Notify the user that the alias 'ai' was added successfully
  echo "Alias 'ai' added successfully."
else
  # Notify the user that the alias 'ai' already exists
  echo "Alias 'ai' already exists."
fi

# Source the updated ~/.bash_profile to make the new alias available immediately
source "$HOME/.bash_profile"
