from __future__ import absolute_import, unicode_literals, print_function, division

import sublime
import sublime_plugin
from . import GitTextCommand

class GitDiffMaster(object):
    def run(self, edit=None, ignore_whitespace=False):
        command = ['git', 'diff', '--no-color', 'HEAD...master']
        if ignore_whitespace:
            command.extend(('--ignore-all-space', '--ignore-blank-lines'))
        command.extend(('--', self.get_file_name()))
        self.run_command(command, self.diff_done)

    def diff_done(self, result):
        if not result.strip():
            self.panel("No output")
            return
        s = sublime.load_settings("Git.sublime-settings")
        syntax = s.get("diff_syntax", "Packages/Diff/Diff.tmLanguage")
        if s.get('diff_panel'):
            self.panel(result, syntax=syntax)
        else:
            self.scratch(result, title="Git Diff", syntax=syntax)

class GitDiffMasterCommand(GitDiffMaster, GitTextCommand):
    pass

