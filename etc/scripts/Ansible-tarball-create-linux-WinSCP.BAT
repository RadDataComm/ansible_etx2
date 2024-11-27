@echo off
@pushd %~dp0
@setlocal
@rem path "c:\apps\winscp429;C:\Program Files (x86)\WinSCP";%path%
set PATH=%PATH%;c:\apps\winscp429;"C:\Program Files (x86)\WinSCP"
@rem WinSCP usage - https://winscp.net/eng/docs/guide_ftp_script_to_sftp#commandline
@rem WinSCP manual https://winscp.net/eng/docs/scriptcommand_mkdir

set USER_NAME=nmsdev
set USER_PSW=nmsdev

@rem /ini - isolate from UI
@rem winscp /script=%~dpn0.SRC /log=%~dpn0.log /ini=nul
@rem open sftp://username:password@sftp.example.com/ -hostkey="-hostkey="ssh-ed25519 256 /rhl1W+dmL8D/hvGr9TZ6neP5aqJIwxm95BgdK9AV5w="" try command line and put inside what we get 
@rem FTP
@rem ascii
@rem put file.txt
@rem WinSCP
@rem put -transfer=ascii file.txt
@rem With SFTP only
@rem Use put -append <localfile> [remotefile].
@rem ftp -v -i -s:%~dpn0.SRC 172.17.171.56
type %~dpn0.SRC | findstr "^open"
@rem In batch, %~dpn0 returns the Drive, Path and Name of the currently executing script.
@rem When specifying /ini=nul, which instructs WinSCP
@rem to ignore the default configuration file and use no configuration at all.
@rem This means it doesn’t load any previously cached data, including known host keys.
@rem WinSCP /script=%~dpn0.SRC /log=%~dpn0.log /ini=nul
echo "WinSCP /script=%~dpn0.SRC /log=%~dpn0.log
WinSCP /script=%~dpn0.SRC /log=%~dpn0.log
@echo off
echo SFTP finished at %DATE% %TIME%
type %~dpn0.SRC | findstr "^open"
echo LOG %~dpn0.log
@endlocal


popd
rem date /T
rem time /T

