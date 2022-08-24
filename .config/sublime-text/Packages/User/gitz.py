# Based on Terminal.py

import sublime
import sublime_plugin
import os
import sys
import subprocess


class OpenGitzCommand(sublime_plugin.WindowCommand):
	def get_path(self, paths):
		if paths:
			return paths[0]
		# DEV: On ST3, there is always an active view.
		#   Be sure to check that it's a file with a path (not temporary view)
		elif self.window.active_view() and self.window.active_view().file_name():
			return self.window.active_view().file_name()
		elif self.window.folders():
			return self.window.folders()[0]
		else:
			sublime.error_message('Terminal: No place to open terminal to')
			return False

	def run(self, paths=[], parameters=None, terminal=None):
		path = self.get_path(paths)
		if not path:
			return

		if os.path.isfile(path):
			path = os.path.dirname(path)

		command=['gitz']
		if parameters is not None:
			command += parameters

		subprocess.Popen(command, cwd=path)

class OpenGitzCurrentFileCommand(OpenGitzCommand):
	def run(self, paths=[], parameters=None, terminal=None):
		if parameters is None:
			path = self.get_path(paths)
			if path and os.path.isfile(path):
				parameters = [path]
		OpenGitzCommand.run(self, paths, parameters, terminal)

