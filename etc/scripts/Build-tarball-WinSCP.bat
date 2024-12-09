@echo off
@rem  <PATH_TO_NETAUTO>\netauto>ansible_etx2\etc\scripts\Ansible-tarball-WinSCP.bat 172.18.178.111
@rem  172.18.178.111 (defaults to this address) LINUX MACHINE where tarball will be built
@rem  optional collection version - will be constructed from galaxy.yml / version:
@rem  optional tarball base name - rad-etx2, will be constructed from galaxy.yml / namespace: and name:
setlocal

set ANSIBLE_PRJ=ansible_etx2

pushd %~dp0..\..

set PRJ_ROOT=%cd%

@rem echo prj root directory is %PRJ_ROOT%
set BUILD_ROOT=%PRJ_ROOT%\etc\.build
if not exist %BUILD_ROOT% md %BUILD_ROOT%
@rem echo build directory %BUILD_ROOT%

cd %BUILD_ROOT%

set WinSCP_SCR=%BUILD_ROOT%\~%ANSIBLE_PRJ%.SCR
set WinSCP_LOG=%BUILD_ROOT%\~%ANSIBLE_PRJ%.log
echo "================================" > %WinSCP_LOG%
echo Script %WinSCP_SCR% >> %WinSCP_LOG%
echo "================================" >> %WinSCP_LOG%

set NETAUTO_LINUX=172.18.178.111
set GALAXY_YML=%PRJ_ROOT%\galaxy.yml
if "%1" NEQ "" set NETAUTO_LINUX=%1

Set PRJ_VERSION=1.0.0
echo searching %GALAXY_YML% for version
Set Set PRJ_VERSION=1.0.0
For /F "tokens=1,2" %%A in ('findstr /C:"version: " %GALAXY_YML%') Do Set PRJ_VERSION=%%B
@rem for version take 3 first elements, not full VERSION. 1.0.0.10 will be handled 1.0.0
@rem For /F "tokens=1,2,3 delims=." %%A in ("%PRJ_VERSION%") Do Set PRJ_VERSION=%%A.%%B.%%C

Set VERSION_INPUT=%PRJ_VERSION%
if "%2" NEQ "" (
	set VERSION_INPUT=%2
)

set NAMESPACE=rad
set MODULE=etx2
set TARBALL_BASE_NAME=namespace-name
if "%3" NEQ "" (
set TARBALL_BASE_NAME=%3
) else (
@rem generic - parse ..\galaxy.yml findstr "namespace: ", "name: ", "version: "
	echo searching %GALAXY_YML% for namesapce and collection name
	if exist %GALAXY_YML% (
		For /F "tokens=1,2" %%A in ('findstr /C:"namespace: " %GALAXY_YML%') Do Set NAMESPACE=%%B
		For /F "tokens=1,2" %%A in ('findstr /C:"name: " %GALAXY_YML%') Do Set NAME=%%B
	)
	set TARBALL_BASE_NAME=%NAMESPACE%-%MODULE%
)

set TARBALL_NAME=%TARBALL_BASE_NAME%-%PRJ_VERSION%.tar.gz

if exist %BUILD_ROOT%\%TARBALL_NAME% del %BUILD_ROOT%\%TARBALL_NAME% 

echo ================================
echo project directory %PRJ_ROOT%
echo build directory %BUILD_ROOT%
echo Linux station %NETAUTO_LINUX%
echo TARBALL_NAME is %TARBALL_NAME%
echo ================================

echo set build version as tag in %GALAXY_YML%
set BUILD_VERSION_TAG=build.version.tag_%VERSION_INPUT%
powershell -Command "(gc %GALAXY_YML%) -replace 'build.version.tag_.*$', '%BUILD_VERSION_TAG%' | Out-File -encoding ASCII %GALAXY_YML%"

set NETAUTO_LINUX_ROOT_DIR=/home/nmsdev/netauto
set NETAUTO_LINUX_DIR=%NETAUTO_LINUX_ROOT_DIR%/%ANSIBLE_PRJ%/%PRJ_VERSION%/%ANSIBLE_PRJ%

echo open sftp://nmsdev:nmsdev@%NETAUTO_LINUX% -hostkey="*" > %WinSCP_SCR%

@rem #-------------------------------------------------------------------------------------
@rem # option batch continue to avoid stop on existing objects and other errors
@rem # still get in log annoying Error creating folder and others but Skip will be applied
@rem #-------------------------------------------------------------------------------------
@rem # Unable to exclude .git folder and .gitignore, so list directories and files we need

echo call rm -rf %NETAUTO_LINUX_DIR% >> %WinSCP_SCR%
echo call rm -f %NETAUTO_LINUX_ROOT_DIR%/tarballs/%TARBALL_NAME%
echo call mkdir -p %NETAUTO_LINUX_DIR%/changelogs >> %WinSCP_SCR%
echo call mkdir -p %NETAUTO_LINUX_DIR%/docs >> %WinSCP_SCR%
@rem echo call mkdir -p %NETAUTO_LINUX_DIR%/etc >> %WinSCP_SCR%
echo call mkdir -p %NETAUTO_LINUX_DIR%/meta >> %WinSCP_SCR%
echo call mkdir -p %NETAUTO_LINUX_DIR%/plugins >> %WinSCP_SCR%
echo call mkdir -p %NETAUTO_LINUX_ROOT_DIR%/tarballs >> %WinSCP_SCR%
echo option transfer ascii >> %WinSCP_SCR%
@rem echo lcd C:\java\build\ems_synergy\root\projects\netauto\%ANSIBLE_PRJ%\etc
@rem echo lcd %~dp0 >> %WinSCP_SCR%
echo put %PRJ_ROOT%\CHANGELOG.rst %NETAUTO_LINUX_DIR%/CHANGELOG.rst >> %WinSCP_SCR%
echo put %PRJ_ROOT%\galaxy.yml %NETAUTO_LINUX_DIR%/galaxy.yml >> %WinSCP_SCR%
echo put %PRJ_ROOT%\LICENSE %NETAUTO_LINUX_DIR%/LICENSE >> %WinSCP_SCR%
echo put %PRJ_ROOT%\README.md %NETAUTO_LINUX_DIR%/README.md >> %WinSCP_SCR%
echo put %PRJ_ROOT%\changelogs %NETAUTO_LINUX_DIR%/changelogs >> %WinSCP_SCR%
echo put %PRJ_ROOT%\docs %NETAUTO_LINUX_DIR%/docs >> %WinSCP_SCR%
@rem echo put %PRJ_ROOT%\etc %NETAUTO_LINUX_DIR%/etc >> %WinSCP_SCR%
echo put %PRJ_ROOT%\meta %NETAUTO_LINUX_DIR%/meta >> %WinSCP_SCR%
echo put %PRJ_ROOT%\plugins %NETAUTO_LINUX_DIR%/plugins >> %WinSCP_SCR%
@rem must ESCAPE &&
echo call cd %NETAUTO_LINUX_DIR% ^&^& ansible-galaxy collection build --force --output-path %NETAUTO_LINUX_ROOT_DIR%/tarballs >> %WinSCP_SCR%
echo option batch continue >> %WinSCP_SCR%
@rem list tar content
@rem echo call tar -tzvf %NETAUTO_LINUX_ROOT_DIR%/tarballs/%TARBALL_NAME% >> %WinSCP_SCR%
echo option transfer binary >> %WinSCP_SCR%
echo get %NETAUTO_LINUX_ROOT_DIR%/tarballs/%TARBALL_NAME% %BUILD_ROOT%\%TARBALL_NAME% >> %WinSCP_SCR%
echo close >> %WinSCP_SCR%
echo exit >> %WinSCP_SCR%
echo call "C:\Program Files (x86)\WinSCP\WinSCP.exe" /script=%WinSCP_SCR% /log=%WinSCP_LOG%
call "C:\Program Files (x86)\WinSCP\WinSCP.exe" /script=%WinSCP_SCR% /log=%WinSCP_LOG%
set /a EXIT_CODE=%ERRORLEVEL%
@rem del %WinSCP_SCR%
@rem del %WinSCP_LOG%
popd
endlocal
exit /B %EXIT_CODE%
