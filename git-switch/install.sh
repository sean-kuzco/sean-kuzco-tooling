# Download the script
curl -O https://raw.githubusercontent.com/sean-kuzco/sean-kuzco-tooling/refs/heads/main/git-switch/git-user-script.py

# Make it executable
chmod +x git-user-script.py

# Move to a directory in PATH for system-wide access
sudo mv git-user-script.py /usr/local/bin/git-user-script

# ----------------------------------------------------------------------------
# Bash Profile Setup:

# Add to ~/.bashrc or ~/.zshrc
# alias gituser='python3 /usr/local/bin/git-user-script'

# Now you can run it from any git repo with:
# gituser