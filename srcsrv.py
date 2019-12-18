import re
import time

from urlparse import urlparse

from base import Environ
from base import Program

class SourceTool:
    program = Program([r"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\srcsrv\srctool.exe", Environ.get_abs_path(r"tools\x64\srcsrv\srctool.exe")])

    def scan_source_paths(self, pdb_path, src_regex):
        src_paths = [src_path.lower() for src_path in self.program.read_pipe(["-r", pdb_path]).splitlines()]
        if src_regex:
            ro = re.compile(src_regex)
            return [src_path for src_path in src_paths if ro.match(src_path)]
        else:
            return src_paths


SVN_FORM = """SRCSRV: ini ------------------------------------------------

VERSION=1
INDEXVERSION=2
VERCTRL=Subversion
DATETIME={0}
SRCSRV: variables ------------------------------------------
SVN_EXTRACT_TARGET=%targ%\%fnbksl%(%var3%)\%var4%\%fnfile%(%var1%)
SVN_EXTRACT_CMD=cmd /c svn.exe cat "%var2%%var3%@%var4%" --non-interactive > "%svn_extract_target%"
SRCSRVTRG=%SVN_extract_target%
SRCSRVCMD=%SVN_extract_cmd%
SRCSRV: source files ---------------------------------------
"""

class SVNIndex:
	program = Program([r"C:\Program Files\TortoiseSVN\bin\svn.exe", Environ.get_abs_path(r"tools\x64\svn\svn.exe")])

	def make_ini(self, dir_path, src_regex, pdb_keys, ini_path):
		def parse_svn_info(block):
			def gen_props(block):
				for line in block.splitlines():
					if len(line) == 0 or line.strip() == "":
						continue
			
					colon_index = line.index(':')
					yield line[:colon_index], line[colon_index + 2:]

			return dict(gen_props(block))

		infos = dict()
		ro = re.compile(src_regex)
		text = self.program.read_pipe(['info', '-R', dir_path])
		blocks = text.split(r"\r\n\r\n")
		for block in blocks:
			info = parse_svn_info(block)
			if info['Node Kind'] == 'file':
				src_path = info['Path']
				key = src_path.lower()
				if ro.match(key):
					infos[key] = info
								
		with open(ini_path, 'w') as out:
			out.write(SVN_FORM.format(time.asctime()))
			
			for key in pdb_keys:
				info = infos[key]
				url = urlparse(info['URL'])
				addr = url.scheme + '://' + url.netloc + '/'
				rel = url.path[1:]
				rev = info['Revision']
				out.write('*'.join((key, addr, rel, rev)) + '\n')

class PDBStr:
	program = Program([r"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\srcsrv\pdbstr.exe", Environ.get_abs_path(r"tools\x64\srcsrv\pdbstr.exe")])

	def bind_index(self, pdb_path, ini_path):
		return self.program.read_pipe(['-w', '-s:srcsrv', '-p:' + pdb_path, '-i:' + ini_path])

	def dump_index(self, pdb_path):
		return self.program.read_pipe(['-r', '-s:srcsrv', '-p:' + pdb_path])


