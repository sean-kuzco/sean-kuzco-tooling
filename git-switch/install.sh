# Download the script
curl -O https://raw.githubusercontent.com/[your-repo]/git-user-switch.py
# Or just save the file above as git-user-switch.py

# Make it executable
chmod +x git-user-script.py

# Move to a directory in PATH for system-wide access
sudo mv git-user-script.py /usr/local/bin/git-user-script

# ----------------------------------------------------------------------------
# Bash Profile Setup:

# Add to ~/.bashrc or ~/.zshrc
# alias gituser='python3 /path/to/git-user-script.py'

# Now you can run it from any git repo with:
# git-user