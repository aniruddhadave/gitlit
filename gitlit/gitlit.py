"""
Implements a light-weight git to commit and push to GitHub.
"""

from gitlit.utils import *
import enum
import os
import sys

class GitLit(enum.Enum):
    commit = 1
    tree = 2
    blob = 3

    def init(repo):
        """Create directory for repo and initialize .git directory."""
        if os.path.isdir(repo):
            """
            @todo: raise exception
            """
            if os.path.isdir(os.path.join(repo, '.git')):
                sys.exit(1)
            else:
                os.mkdir(os.path.join(repo, 'git'))
        else:
            os.mkdir(repo)
            os.mkdir(os.path.join(repo, 'git'))
        
        for name in ['objects', 'refs', 'refs/heads']:
            os.mkdir(os.path.join(repo, '.git', name))
        write_file(os.path.join(repo, '.git', 'HEAD'), b'ref: refs/heads/master')
        print('Initialized empty repository: {}'.format(repo))
        