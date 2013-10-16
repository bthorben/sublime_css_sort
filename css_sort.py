import sublime
import sublime_plugin
import sys
import os

directory = os.path.dirname(os.path.realpath(__file__))
directory = os.path.join(directory, "libs")
if directory not in sys.path:
    sys.path.append(directory)

from csssort_wrapper import CssSortWrapper

settings = sublime.load_settings("websuite.sublime-settings")


def get_type(view):
    fName = view.file_name()
    vSettings = view.settings()
    syntaxPath = vSettings.get('syntax')
    syntax = ""
    ext = ""

    if fName is not None:
        # file exists, pull syntax type from extension
        ext = os.path.splitext(fName)[1][1:]
    if syntaxPath is not None:
        syntax = os.path.splitext(syntaxPath)[0].split('/')[-1].lower()

    if ext in ['css'] or "css" in syntax:
        return "css"


def is_supported(view):
    return get_type(view) in ["css"]


class WebSuiteFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not is_supported(self.view):
            return
        w = CssSortWrapper(self.view)
        w.sortcss(edit)

    def is_enabled(self):
        return is_supported(self.view)
