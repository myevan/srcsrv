# 윈도우 디버깅 도구 (Windows Debugging Tools Helper)

## SVN 소스 인덱스

```bat
C:\Works\windbg> cli.bat make-svn-index C:\Works\Hello\bin\x64\Hello.pdb C:\Works\Hello\src --src-regex="c:\\work\\hello\\[\w\\\.]+(.cpp|.c|.h)"
```

## PDB 인덱스 확인

```bat
C:\Works\windbg> cli.bat show-pdb-index C:\Works\Hello\bin\x64\Hello.pdb
```
