#!/usr/bin/env python3
"""
git-user-switch: A CLI tool for managing multiple Git users in a repository
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from getpass import getpass


class GitUserSwitcher:
    def __init__(self):
        # Store users in a JSON file in the git repo's .git directory
        self.git_dir = self._find_git_dir()
        if not self.git_dir:
            print("Error: Not in a Git repository")
            sys.exit(1)
        
        self.users_file = self.git_dir / "git-users.json"
        self.users = self._load_users()
    
    def _find_git_dir(self):
        """Find the .git directory in current or parent directories"""
        current = Path.cwd()
        while current != current.parent:
            git_dir = current / ".git"
            if git_dir.exists() and git_dir.is_dir():
                return git_dir
            current = current.parent
        return None
    
    def _load_users(self):
        """Load users from JSON file"""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def _save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def _run_git_command(self, *args):
        """Run a git command and return output"""
        try:
            result = subprocess.run(
                ['git'] + list(args),
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None
    
    def get_current_user(self):
        """Get current Git user from local config"""
        name = self._run_git_command('config', '--local', 'user.name')
        email = self._run_git_command('config', '--local', 'user.email')
        return name, email
    
    def set_git_user(self, name, email):
        """Set Git user in local config"""
        self._run_git_command('config', '--local', 'user.name', name)
        self._run_git_command('config', '--local', 'user.email', email)
        print(f"\n✓ Switched to: {name} <{email}>")
    
    def display_current_user(self):
        """Display current Git user"""
        name, email = self.get_current_user()
        if name and email:
            print(f"\n🔧 Current Git user: {name} <{email}>")
        else:
            print("\n⚠️  No Git user configured in this repository")
    
    def list_users(self):
        """List all stored users"""
        if not self.users:
            print("\n📭 No users saved yet")
            return False
        
        print("\n👥 Saved users:")
        for i, (name, info) in enumerate(self.users.items(), 1):
            print(f"  {i}. {name} <{info['email']}>")
        return True
    
    def change_user(self):
        """Change to another user"""
        if not self.list_users():
            print("Add a user first!")
            return
        
        print("\nSelect a user (number) or 0 to cancel:")
        try:
            choice = int(input("Choice: "))
            if choice == 0:
                return
            
            users_list = list(self.users.items())
            if 1 <= choice <= len(users_list):
                name, info = users_list[choice - 1]
                self.set_git_user(name, info['email'])
            else:
                print("Invalid choice")
        except (ValueError, IndexError):
            print("Invalid input")
    
    def add_user(self):
        """Add a new user"""
        print("\n➕ Add new user")
        name = input("Name (e.g., 'John Doe'): ").strip()
        if not name:
            print("Name cannot be empty")
            return
        
        email = input("Email: ").strip()
        if not email or '@' not in email:
            print("Invalid email address")
            return
        
        # Note: Git doesn't use passwords for commits, only for remote operations
        # Storing this for potential future use with credential helpers
        print("\nNote: Password is optional and only used for remote operations")
        password = getpass("Password (press Enter to skip): ").strip()
        
        self.users[name] = {
            'email': email,
            'password': password if password else None
        }
        self._save_users()
        
        print(f"\n✓ Added user: {name} <{email}>")
        
        # Ask if they want to switch to this user now
        switch = input("Switch to this user now? (y/n): ").lower()
        if switch == 'y':
            self.set_git_user(name, email)
    
    def remove_user(self):
        """Remove a user"""
        if not self.list_users():
            return
        
        print("\nSelect a user to remove (number) or 0 to cancel:")
        try:
            choice = int(input("Choice: "))
            if choice == 0:
                return
            
            users_list = list(self.users.keys())
            if 1 <= choice <= len(users_list):
                name = users_list[choice - 1]
                confirm = input(f"Remove {name}? (y/n): ").lower()
                if confirm == 'y':
                    del self.users[name]
                    self._save_users()
                    print(f"✓ Removed user: {name}")
            else:
                print("Invalid choice")
        except (ValueError, IndexError):
            print("Invalid input")
    
    def run(self):
        """Main CLI loop"""
        print("\n" + "="*50)
        print("🔄 Git User Switcher")
        print("="*50)
        
        while True:
            self.display_current_user()
            
            print("\nOptions:")
            print("  1. Change to another user")
            print("  2. Add a new user")
            print("  3. Remove a user")
            print("  4. Exit")
            
            try:
                choice = input("\nSelect option (1-4): ").strip()
                
                if choice == '1':
                    self.change_user()
                elif choice == '2':
                    self.add_user()
                elif choice == '3':
                    self.remove_user()
                elif choice == '4':
                    print("\n👋 Goodbye!")
                    break
                else:
                    print("Invalid option. Please choose 1-4.")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Entry point"""
    try:
        switcher = GitUserSwitcher()
        switcher.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()