#!/usr/bin/env python3


import os
import hashlib
import json
import shutil
from datetime import datetime
import sys

def hash_object(content):
    return hashlib.sha1(content.encode()).hexdigest()

class VCS:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.vcs_path = os.path.join(repo_path, '.vcs')
        self.objects_path = os.path.join(self.vcs_path, 'objects')
        self.refs_path = os.path.join(self.vcs_path, 'refs')
        self.index_path = os.path.join(self.vcs_path, 'index')
        self.ignore_file = os.path.join(self.vcs_path, '.vcsignore')

    def init(self):
        if os.path.exists(self.vcs_path):
            print("Repository already initialized.")
            return

        os.makedirs(self.objects_path)
        os.makedirs(self.refs_path)
        with open(self.index_path, 'w') as index_file:
            index_file.write(json.dumps({}))
        with open(self.ignore_file, 'w') as ignore_file:
            ignore_file.write("")
        self._write_ref('HEAD', 'master')
        print("Initialized empty VCS repository.")

    def _write_ref(self, ref, content):
        with open(os.path.join(self.refs_path, ref), 'w') as ref_file:
            ref_file.write(content)

    def _read_ref(self, ref):
        breakpoint()
        try:
            with open(os.path.join(self.refs_path, ref), 'r') as ref_file:
                return ref_file.read().strip()
        except FileNotFoundError:
            return None

    def _read_index(self):
        with open(self.index_path, 'r') as index_file:
            return json.loads(index_file.read())

    def _write_index(self, index):
        with open(self.index_path, 'w') as index_file:
            index_file.write(json.dumps(index, indent=2))

    def add(self, filepath):
        if self._is_ignored(filepath):
            print(f"Ignoring file: {filepath}")
            return

        with open(filepath, 'r') as f:
            content = f.read()
        file_hash = hash_object(content)

        # Write to objects directory
        object_path = os.path.join(self.objects_path, file_hash)
        with open(object_path, 'w') as obj_file:
            obj_file.write(content)

        # Update index
        index = self._read_index()
        relative_path = os.path.relpath(filepath, self.repo_path)
        index[relative_path] = file_hash
        self._write_index(index)
        print(f"Staged {filepath}")

    def commit(self, message):
        index = self._read_index()
        if not index:
            print("Nothing to commit.")
            return

        parent_commit = self._read_ref('HEAD')
        commit_content = {
            'tree': index,
            'parent': parent_commit,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }

        commit_hash = hash_object(json.dumps(commit_content))

        with open(os.path.join(self.objects_path, commit_hash), 'w') as commit_file:
            commit_file.write(json.dumps(commit_content, indent=2))

        self._write_ref('HEAD', commit_hash)
        print(f"Committed as {commit_hash[:7]}: {message}")

    def log(self):
        commit_hash = self._read_ref('HEAD')
        while commit_hash:
            with open(os.path.join(self.objects_path, commit_hash), 'r') as commit_file:
                commit = json.load(commit_file)
            print(f"Commit {commit_hash[:7]}:")
            print(f"  Message: {commit['message']}")
            print(f"  Timestamp: {commit['timestamp']}")
            print()
            commit_hash = commit['parent']

    def _is_ignored(self, filepath):
        with open(self.ignore_file, 'r') as ignore_file:
            ignored_patterns = ignore_file.read().splitlines()
        relative_path = os.path.relpath(filepath, self.repo_path)
        return any(relative_path.startswith(pattern) for pattern in ignored_patterns)

    def branch(self, name):
        head_commit = self._read_ref('HEAD')
        self._write_ref(name, head_commit)
        print(f"Created branch {name}.")

    def checkout(self, branch):
        commit_hash = self._read_ref(branch)
        if not commit_hash:
            print(f"Branch {branch} does not exist.")
            return
        self._write_ref('HEAD', branch)
        print(f"Switched to branch {branch}.")

    def status(self):
        print("Current status of the repository:")
        print(f"HEAD: {self._read_ref('HEAD')}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ./vcs.py <command> <args>")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'init' and len(sys.argv) > 2:
        print("Usage: python ./vcs.py <command> <args>")
        sys.exit(1)

    repo_path = os.getcwd()
    vcs = VCS(repo_path)

    if command == "init":
        vcs.init()
    elif command == "add":
        filepath = sys.argv[2]
        vcs.add(filepath)
    elif command == "commit":
        message = sys.argv[2]
        vcs.commit(message)
    elif command == "log":
        vcs.log()
    elif command == "branch":
        branch_name = sys.argv[2]
        vcs.branch(branch_name)
    elif command == "checkout":
        branch_name = sys.argv[2]
        vcs.checkout(branch_name)
    elif command == "status":
        vcs.status()
    else:
        print(f"Unknown command: {command}")
