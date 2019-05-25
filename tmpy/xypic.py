#!/usr/bin/env python
###############################################################################
##
## MODULE      : xypic.py
## DESCRIPTION : XYpic plotting support
## COPYRIGHT   : (C) 2019  Darcy Shen
##               (C) 2004 Nicolas Ratier (nicolas DOT ratier AT lpmo DOT edu)
##               (C) XYpic latex package Kristoffer H. Rose
##
## This software falls under the GNU general public license version 3 or later.
## It comes WITHOUT ANY WARRANTY WHATSOEVER. For details, see the file LICENSE
## in the root directory or <http://www.gnu.org/licenses/gpl-3.0.html>.

import os
from subprocess import Popen, PIPE, STDOUT
from .graph import Graph
from .protocol import *


class XYpic(Graph):
    def __init__(self, name = "xypic"):
        super(XYpic, self).__init__()
        self.name = name

        self.pre_code = """
\\documentclass{article}
\\usepackage[all]{xy}
\\pagestyle{empty}
\\begin{document}
"""
        self.post_code = "\end{document}"
        self.message = "TeXmacs interface to XYpic (high level 2-dimensional graphics)"
        self.width = "640px"

    def evaluate(self, code):
        code_path = self.get_tmp_dir() + self.name + ".tex"
        dvi_path = self.get_tmp_dir() + self.name + ".dvi"
        with open(code_path, 'w') as code_file:
            code_file.write(self.pre_code)
            code_file.write("\n")
            code_file.write(code)
            code_file.write("\n")
            code_file.write(self.post_code)

        cmd0 = ["latex", "--interaction=nonstopmode", code_path]
        cmd1 = ["dvips", "-q", "-f", "-E", dvi_path, "-o", self.get_eps_path()]
        Popen(cmd0, stdout=os.open(os.devnull, os.O_RDWR), stderr=PIPE).communicate()
        p = Popen(cmd1, stdout=os.open(os.devnull, os.O_RDWR), stderr=PIPE)
        out, err = p.communicate()
        if (p.returncode == 0):
            flush_file (self.get_eps())
        else:
            flush_verbatim (err)

