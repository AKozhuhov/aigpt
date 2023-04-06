#!/bin/bash

# Check if the alias already exists in the ~/.bash_profile
if ! grep -q "alias aii=" "$HOME/.bash_profile"; then
  # Add the alias to the ~/.bash_profile
	dir="$(pwd)"
  echo "alias ai='python3 $dir/main.py'" >> "$HOME/.bash_profile"
  echo "Alias 'ai' added successfully."
else
  echo "Alias 'ai' already exists."
fi

# Source the updated ~/.bash_profile
source "$HOME/.bash_profile"
