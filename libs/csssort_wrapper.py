import sublime
import sys
import os

directory = os.path.dirname(os.path.realpath(__file__))
if directory not in sys.path:
    sys.path.append(directory)

import css_sort
import merge_utils


class CssSortWrapper:

    def __init__(self, view):
        self.view = view

    def sort(self, code):
        return css_sort.sort(code)

    def sortcss(self, edit):
        selection = self.view.sel()[0]
        hasSelection = len(selection) > 0

        if hasSelection:
            self.__format_selection__(edit)
        else:
            self.__format_whole_file__(edit)

    def __format_whole_file__(self, edit):
        view = self.view
        region = sublime.Region(0, view.size())
        code = view.substr(region)
        sorted_code = self.sort(code)
        _, err = merge_utils.merge_code(view, edit, code, sorted_code)
        if err:
            print("CSS-Sort Format: Merge failure: '%s'" % err)

    def __format_selection__(self, edit):
        def get_line_indentation_pos(point):
            line_region = self.view.line(point)
            pos = line_region.a
            end = line_region.b
            while pos < end:
                ch = self.view.substr(pos)
                if ch != ' ' and ch != '\t':
                    break
                pos += 1
            return pos

        regions = []
        for sel in self.view.sel():
            start = get_line_indentation_pos(min(sel.a, sel.b))
            region = sublime.Region(
                self.view.line(start).a,
                self.view.line(max(sel.a, sel.b)).b)
            code = self.view.substr(region)
            sorted_code = self.sort(code)
            self.view.replace(edit, region, sorted_code)
            if sel.a <= sel.b:
                regions.append(sublime.Region(region.a,
                                              region.a + len(sorted_code)))
            else:
                regions.append(sublime.Region(region.a + len(sorted_code),
                                              region.a))
        self.view.sel().clear()
        [self.view.sel().add(region) for region in regions]
