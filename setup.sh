#!/bin/bash

# Make the Python script executable
chmod +x go2web.py

# Create a symbolic link
sudo ln -s "$(pwd)/go2web.py" /usr/local/bin/go2web

echo "Application setup completed."
echo "You can now run the program using the command 'go2web'."