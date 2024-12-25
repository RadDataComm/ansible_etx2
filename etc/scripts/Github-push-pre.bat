@echo off
echo prepare github push, mainly prevent etc directory push
@rem  copy the ansible_etx2 project to ansible_etx2_github
@rem  update .gitignore - add etc/
@rem remove from staging etc directory and commit with message "GITHUB preparation, remove etc"
@rem issue 3 git commands (use set-url)
@rem git remote set-url origin https://github.com/RadDataComm/ansible_etx2.git
@rem git branch -M main
@rem git push -u origin main
setlocal EnableExtensions EnableDelayedExpansion
echo prepare github push
set GITHUB_URL_RADDATACOMM=https://github.com/RadDataComm
set ANSIBLE_PRJ=ansible_etx2
set GIT_REMOTE=%GITHUB_URL_RADDATACOMM%/%ANSIBLE_PRJ%.git
echo remote set to %GIT_REMOTE%
pushd %~dp0..\..
set PRJ_ROOT=%cd%
set PRJ_ROOT_GITHUB=%~dp0..\..\..\%ANSIBLE_PRJ%_GITHUB
echo PRJ_ROOT_GITHUB is %PRJ_ROOT_GITHUB%
if exist %PRJ_ROOT_GITHUB% rmdir /S /Q %PRJ_ROOT_GITHUB%
md %PRJ_ROOT_GITHUB%
xcopy /s /e /h /q %PRJ_ROOT% %PRJ_ROOT_GITHUB%
cd %PRJ_ROOT_GITHUB%
IF %ERRORLEVEL% NEQ 0 (
echo cannot changedir to %PRJ_ROOT_GITHUB%, exit
goto _exit
) else (
set PRJ_ROOT_GITHUB=%cd%
)
echo etc/ >> %PRJ_ROOT_GITHUB%\.gitignore
set EXIT_CODE=1
git --version
IF %ERRORLEVEL% NEQ 0 (
echo git not found exit
) else (
echo git remove etc from staging
git rm -r --cached etc/
git commit -m "GITHUB preparation, removed etc"
set /a EXIT_CODE=%ERRORLEVEL%
echo push to github uncomment or run manually following git commands - see in batch
@rem git remote set-url origin %GIT_REMOTE%
@rem git branch -M main
@rem git push -u origin main
@rem set /a EXIT_CODE=%ERRORLEVEL%
)
echo EXIT CODE is %EXIT_CODE%
if %EXIT_CODE% EQU 0 goto exit_
popd
:exit_error
echo prepare github push failed
:exit_
if exist %PRJ_ROOT_GITHUB% echo remove manually %PRJ_ROOT_GITHUB%!
@rem rmdir /S /Q %PRJ_ROOT_GITHUB%

endlocal
exit /B %EXIT_CODE%
