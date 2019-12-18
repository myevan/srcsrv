import os
import subprocess

class Environ:
    inst = None

    @classmethod
    def get_abs_path(cls, rel_path):
        return os.path.normpath(os.path.join(cls.get().this_dir_path, rel_path))

    @classmethod
    def get(cls):
        if not cls.inst:
            cls.inst = cls(__file__)
        return cls.inst

    def __init__(self, this_file_path):
        self.this_dir_path = os.path.normpath(os.path.dirname(os.path.realpath(this_file_path)))
        

class Program:
    def __init__(self, exe_paths):
        for exe_path in exe_paths:
            if os.path.isfile(exe_path):
                self.exe_path = exe_path
                break
        else:
            raise RuntimeError("NO_EXE_PATH:" + repr(exe_paths))

    def read_pipe(self, args, check=False):
        proc = subprocess.Popen([self.exe_path] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        return out


