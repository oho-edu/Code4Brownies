# Code4Brownies - Student module
# Author: Vinhthuy Phan, 2015-2017
#
import sublime, sublime_plugin
import urllib.parse
import urllib.request
import os
import json
import threading
import time

c4b_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "info")
c4b_REGISTER_PATH = "register"
c4b_SHARE_PATH = "share"
c4b_MY_POINTS_PATH = "my_points"
c4b_RECEIVE_BROADCAST_PATH = "receive_broadcast"
c4b_CHECK_BROADCAST_PATH = "check_broadcast"

TIMEOUT = 10
RUNNING_BACKGROUND_TASK = False

# ------------------------------------------------------------------
def c4b_get_attr():
	try:
		with open(c4b_FILE, 'r') as f:
			json_obj = json.loads(f.read())
	except:
		sublime.message_dialog("Please set information first.")
		return None
	if 'Server' not in json_obj or 'Name' not in json_obj:
		sublime.message_dialog("Please set information completely.")
		return None
	if not json_obj['Server'].startswith("http://"):
		sublime.message_dialog("Server must starts with http://\nReset information.")
		return None
	return json_obj

# ------------------------------------------------------------------
def c4bRequest(url, data):
	req = urllib.request.Request(url, data)
	try:
		with urllib.request.urlopen(req, None, TIMEOUT) as response:
			return response.read().decode(encoding="utf-8")
	except urllib.error.URLError as err:
		sublime.message_dialog("{0}\nPossibly server not running or incorrect server address.".format(err))
		return None

# ------------------------------------------------------------------
def check_with_server():
	MAX_POLLING_TIME = 2700  # 90 minutes
	SLEEP_TIME, TOTAL_SLEEP_TIME = 120, 0
	RUNNING_BACKGROUND_TASK = True
	while TOTAL_SLEEP_TIME < MAX_POLLING_TIME:
		info = c4b_get_attr()
		if info is None:
			return
		url = urllib.parse.urljoin(info['Server'], c4b_CHECK_BROADCAST_PATH)
		values = {'uid':info['Name']}
		data = urllib.parse.urlencode(values).encode('ascii')
		req = urllib.request.Request(url, data)
		try:
			with urllib.request.urlopen(req, None, TIMEOUT) as r:
				response = r.read().decode(encoding="utf-8")
				print(response)
				if response == "true":
					sublime.status_message("Your whiteboard has been updated!")
					# _receive_broadcast(self, edit, info['Name'])
					# sublime.run_command('c4b_my_board')
		except urllib.error.URLError as err:
			print("Cannot connect with server. Stop polling.")
			break
		TOTAL_SLEEP_TIME += SLEEP_TIME
		time.sleep(SLEEP_TIME)
	RUNNING_BACKGROUND_TASK = False

# ------------------------------------------------------------------
def background_task():
	bg_thread = threading.Thread(target=check_with_server)
	bg_thread.start()

# ------------------------------------------------------------------
class c4bAutoUpdateBoardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		background_task()

# ------------------------------------------------------------------
def _receive_broadcast(edit, uid):
	info = c4b_get_attr()
	if info is None:
		return
	data = urllib.parse.urlencode({'uid':uid}).encode('ascii')
	url = urllib.parse.urljoin(info['Server'], c4b_RECEIVE_BROADCAST_PATH)
	response = c4bRequest(url, data)
	if response != "":
		json_obj = json.loads(response)
		content = json_obj['content']
		if len(content.strip()) > 0:
			new_view = sublime.active_window().new_file()
			new_view.insert(edit, 0, content)
		else:
			if uid=='':
				sublime.message_dialog("Whiteboard is empty.")
			else:
				sublime.message_dialog("Your board is empty.")
	else:
		sublime.message_dialog("Register, if you have not done so.")

# ------------------------------------------------------------------
class c4bMyBoardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		info = c4b_get_attr()
		if info is None:
			return
		_receive_broadcast(edit, info['Name'])

# ------------------------------------------------------------------
class c4bShareCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		info = c4b_get_attr()
		if info is None:
			return
		url = urllib.parse.urljoin(info['Server'], c4b_SHARE_PATH)

		# Guesstimate extension
		this_file_name = self.view.file_name()
		header = ''
		if this_file_name is not None:
			lines = open(this_file_name).readlines()
			if len(lines)>0 and (lines[0].startswith('#') or lines[0].startswith('//')):
				header = lines[0]
			if '.' not in this_file_name:
				ext = ''
			else:
				ext = this_file_name.split('.')[-1]
		else:
			ext = 'py'

		# Determine content
		content = ''.join([ self.view.substr(s) for s in self.view.sel() ])
		if len(content) < 10:  # probably selected by mistake
			content = self.view.substr(sublime.Region(0, self.view.size()))
		else:
			content = header + '\n' + content

		# Now send
		values = {'uid':info['Name'], 'body':content, 'ext':ext, 'mode': 'code'}
		data = urllib.parse.urlencode(values).encode('ascii')
		response = c4bRequest(url,data)
		if response is not None:
			sublime.message_dialog(response)

# ------------------------------------------------------------------
class c4bVote(sublime_plugin.WindowCommand):
	def run(self):
		sublime.active_window().show_input_panel("ENTER to Vote or ESC to Cancel.",
			"",
			self.vote,
			None,
			None)

	def vote(self, answer):
		answer = answer.strip()
		if len(answer) > 0:
			info = c4b_get_attr()
			if info is None:
				return
			url = urllib.parse.urljoin(info['Server'], c4b_SHARE_PATH)
			values = {'uid':info['Name'], 'body':answer, 'ext':'', 'mode': 'poll'}
			data = urllib.parse.urlencode(values).encode('ascii')
			response = c4bRequest(url,data)
			if response is not None:
				sublime.message_dialog(response)
		else:
			sublime.message_dialog("Answer cannot be empty.")

# ------------------------------------------------------------------
class c4bRegister(sublime_plugin.WindowCommand):
	def run(self):
		info = c4b_get_attr()
		if info is None:
			sublime.message_dialog("Please Set Information.")
		else:
			url = urllib.parse.urljoin(info['Server'], c4b_REGISTER_PATH)
			values = {'uid':info['Name']}
			data = urllib.parse.urlencode(values).encode('ascii')
			response = c4bRequest(url,data)
			if response is not None:
				sublime.message_dialog(response)

# ------------------------------------------------------------------
class c4bShowPoints(sublime_plugin.WindowCommand):
	def run(self):
		info = c4b_get_attr()
		if info is None:
			return
		url = urllib.parse.urljoin(info['Server'], c4b_MY_POINTS_PATH)
		values = {'uid':info['Name']}
		data = urllib.parse.urlencode(values).encode('ascii')
		response = c4bRequest(url,data)
		if response is not None:
			sublime.message_dialog(response)

# ------------------------------------------------------------------
class c4bSetInfo(sublime_plugin.WindowCommand):
	def run(self):
		try:
			with open(c4b_FILE, 'r') as f:
				info = json.loads(f.read())
		except:
			info = dict()

		if 'Name' not in info:
			info['Name'] = 'JohnSmith'
		if 'Server' not in info:
			info['Server'] = 'http://0.0.0.0:4030'

		with open(c4b_FILE, 'w') as f:
			f.write(json.dumps(info, indent=4))

		sublime.active_window().open_file(c4b_FILE)

# ------------------------------------------------------------------
class c4bAbout(sublime_plugin.WindowCommand):
	def run(self):
		try:
			version = open(os.path.join(sublime.packages_path(), "C4BStudent", "VERSION")).read().strip()
		except:
			version = 'Unknown'
		sublime.message_dialog("Code4Brownies (v%s)\nCopyright 2015-2017 Vinhthuy Phan" % version)

# ------------------------------------------------------------------
class c4bUpgrade(sublime_plugin.WindowCommand):
	def run(self):
		if sublime.ok_cancel_dialog("Are you sure you want to upgrade Code4Brownies to the latest version?", "Yes"):
			package_path = os.path.join(sublime.packages_path(), "C4BStudent")
			if not os.path.isdir(package_path):
				os.mkdir(package_path)
			c4b_py = os.path.join(package_path, "Code4Brownies.py")
			c4b_menu = os.path.join(package_path, "Main.sublime-menu")
			c4b_version = os.path.join(package_path, "VERSION")
			try:
				urllib.request.urlretrieve("https://raw.githubusercontent.com/vtphan/Code4Brownies/master/src/C4BStudent/Code4Brownies.py", c4b_py)
				urllib.request.urlretrieve("https://raw.githubusercontent.com/vtphan/Code4Brownies/master/src/C4BStudent/Main.sublime-menu", c4b_menu)
				urllib.request.urlretrieve("https://raw.githubusercontent.com/vtphan/Code4Brownies/master/src/VERSION", c4b_version)
				version = open(c4b_version).read()
				sublime.message_dialog("Code4Brownies has been upgraded to version %s" % version)
			except:
				sublime.message_dialog("A problem occurred during upgrade.")