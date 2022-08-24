# Based on Default/copy_path.py 

import sublime
import sublime_plugin
import subprocess
import os.path
import re

def getGitOutput(args, context):
	proc = subprocess.run([
		'git',
		'-C', context,
		*args,
	], capture_output=True)
	if proc.returncode != 0:
		raise Exception('CopyGithubLink', proc.stderr.decode('utf-8'))
	output = proc.stdout.decode('utf-8').strip()
	print('CopyGithubLink', output)
	if len(output) == 0:
		raise Exception('CopyGithubLink', output, 'is empty')
	return output

def formatSelectedLine(view, lineFormat="#L{}", mutiLineFormat="#L{}-L{}"):
	sel = view.sel()
	print(sel)
	start = sel[0].begin()
	end = sel[0].end()
	start = view.rowcol(start)[0] + 1
	end = view.rowcol(end)[0] + 1
	if start == end:
		return lineFormat.format(start)
	else:
		return mutiLineFormat.format(start, end)

class CopyGithubLinkCommand(sublime_plugin.TextCommand):
	def run(self, edit, selectedLine=False):
		if len(self.view.file_name()) == 0:
			return
		filepath = self.view.file_name()
		dirpath = os.path.dirname(filepath)

		originUrl = getGitOutput([
			'config', '--local', '--get', 'remote.origin.url',
		], context=dirpath)
		branchRef = getGitOutput([
			'rev-parse', '--abbrev-ref', 'HEAD',
		], context=dirpath)
		relFilepath = getGitOutput([
			'ls-files', '--full-name', filepath,
		], context=dirpath)

		# originUrl='git@github.com:Zren/mpvz.git'
		# branchRef='master' # Assume

		website = ''
		link = ''

		m = re.match('^(git\@github\.com\:|https\:\/\/github\.com\/)([^\/]+)\/([^\/]+)\.git$', originUrl)
		if m:
			website = 'GitHub'
			userName = m.group(2)
			repoName = m.group(3)
			link = 'https://github.com/{}/{}/blob/{}/{}'.format(
				userName,
				repoName,
				branchRef,
				relFilepath,
			)
			if selectedLine:
				link += formatSelectedLine(self.view, mutiLineFormat="#L{}-L{}")


		m = re.match('^(kde\:|git\@invent\.kde\.org\:|https\:\/\/invent\.kde\.org\/)([^\/]+)\/([^\/]+)\.git$', originUrl)
		if m:
			website = 'GitLab'
			userName = m.group(2)
			repoName = m.group(3)
			link = 'https://invent.kde.org/{}/{}/-/blob/{}/{}'.format(
				userName,
				repoName,
				branchRef,
				relFilepath,
			)
			if selectedLine:
				link += formatSelectedLine(self.view, mutiLineFormat="#L{}-{}")

		if link:
			print("link", link)
			sublime.set_clipboard(link)
			sublime.status_message("Copied {} Link".format(website))


	def is_enabled(self):
		if self.view.file_name() is None:
			return False
		if len(self.view.file_name()) == 0:
			return False
		return True
