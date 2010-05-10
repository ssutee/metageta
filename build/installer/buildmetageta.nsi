
    ######################################################################
    #      NSIS Installation Script
    #
    #       This install script requires the following symbols to be
    #       defined via the /D commandline switch. It is usually run
    #       by the buildmetageta.py script:
    #
    #       EXCLUDE           Relative path to the MetaGETA code
    #       APP_DIR           Relative path to the MetaGETA code
    #       BIN_DIR           Relative path to the GDAL & Python directory
    #       VERSION           N.N.N.N format version number
    #       DISPLAY_VERSION   Version text string
    #       OUTPATH           Output installer filepath
    #
    #       Example:
    #       makensis /DVERSION=1.2.0.123 /DDISPLAY_VERSION=1.2 RC1 /DOUTPATH=..\downloads\metageta-1.2-setup.exe /DBIN_DIR=..\bin /DAPP_DIR=tmp buildmetageta.nsi
    #
    ######################################################################
    !define /date YEAR "%Y"

    !define APP_NAME "MetaGETA"
    !define COMP_NAME "Department of Environment, Heritage, Water and the Arts"
    !define WEB_SITE "http://code.google.com/p/metageta"
    !define COPYRIGHT "${COMP_NAME} � ${YEAR}"
    !define DESCRIPTION "MetaGETA installer (Metadata Gathering, Extraction and Transformation Application)"
    !define LICENSE_TXT "licenses\license.rtf"
    !define MUI_WELCOMEFINISHPAGE_BITMAP "graphics\installer.bmp"
    !define REG_START_MENU "Start Menu Folder"
    !define MUI_ICON "graphics\metageta.ico"

    var StartMenuFolder

    ######################################################################

    SetCompressor LZMA
    Name "${APP_NAME}"
    Caption "${APP_NAME}"
    OutFile "${OUTPATH}"
    BrandingText "${APP_NAME}"
    XPStyle on

    ######################################################################

    !define INSTALL_PATH "Software\${APP_NAME}"
    !define UNINSTALL_PATH "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    !define MULTIUSER_EXECUTIONLEVEL Highest
    !define MULTIUSER_MUI
    !define MULTIUSER_INSTALLMODE_COMMANDLINE
    !define MULTIUSER_INSTALLMODE_INSTDIR "${APP_NAME}"
    !define MULTIUSER_INSTALLMODE_DEFAULT_REGISTRY_KEY "${UNINSTALL_PATH}"
    !define MULTIUSER_INSTALLMODE_DEFAULT_REGISTRY_VALUENAME "UninstallString"
    !define MULTIUSER_INSTALLMODE_INSTDIR_REGISTRY_KEY "${INSTALL_PATH}"
    !define MULTIUSER_INSTALLMODE_INSTDIR_REGISTRY_VALUENAME "InstallLocation"
    !define REG_ROOT "SHCTX"

    !include "FileFunc.nsh"

    !include "MultiUser.nsh"
    !include "MUI.nsh"

    !define MUI_ABORTWARNING
    !define MUI_UNABORTWARNING

    ######################################################################

    !ifdef VERSION
        VIProductVersion  "${VERSION}"
        VIAddVersionKey "FileVersion"  "${VERSION}"
        VIAddVersionKey "ProductName"  "${APP_NAME}"
        VIAddVersionKey "CompanyName"  "${COMP_NAME}"
        VIAddVersionKey "LegalCopyright"  "${COPYRIGHT}"
        VIAddVersionKey "FileDescription"  "${DESCRIPTION}"
    !endif

    ######################################################################

    !insertmacro MUI_PAGE_WELCOME
    !insertmacro MUI_PAGE_LICENSE "${LICENSE_TXT}"
    !insertmacro MULTIUSER_PAGE_INSTALLMODE
    !insertmacro MUI_PAGE_DIRECTORY

    !ifdef REG_START_MENU
        !define MUI_STARTMENUPAGE_DEFAULTFOLDER "${APP_NAME}"
        !define MUI_STARTMENUPAGE_REGISTRY_ROOT "${REG_ROOT}"
        !define MUI_STARTMENUPAGE_REGISTRY_KEY "${UNINSTALL_PATH}"
        !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "${REG_START_MENU}"
        !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
    !endif

    !insertmacro MUI_PAGE_INSTFILES
    !insertmacro MUI_PAGE_FINISH
    !insertmacro MUI_UNPAGE_CONFIRM
    !insertmacro MUI_UNPAGE_INSTFILES
    !insertmacro MUI_UNPAGE_FINISH
    !insertmacro MUI_LANGUAGE "English"

    ######################################################################
    ; The "" makes the section hidden.
    Section "" SecUninstallPrevious
        Call UninstallPrevious
    SectionEnd

    Section -MainProgram
        ;${INSTALL_TYPE}
        SetOverwrite ifnewer
        SetOutPath $INSTDIR
        File /r ${EXCLUDE} "${APP_DIR}\*"
        ${GetFileName} "${BIN_DIR}" $R0
        SetOutPath $INSTDIR\$R0
        File /r  ${EXCLUDE} "${BIN_DIR}\*"
    SectionEnd


    ######################################################################

    Section -Icons_Reg
        SetOutPath "$INSTDIR"
        WriteUninstaller "$INSTDIR\Uninstall.exe"

        !ifdef REG_START_MENU
            !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
                CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
                CreateShortCut  "$SMPROGRAMS\$StartMenuFolder\Run Crawler.lnk" "$INSTDIR\metageta\runcrawler.bat" "" "$INSTDIR\metageta\lib\wm_icon.ico" 0 SW_SHOWMINIMIZED
                CreateShortCut  "$SMPROGRAMS\$StartMenuFolder\Run Transform.lnk" "$INSTDIR\metageta\runtransform.bat" "" "$INSTDIR\metageta\lib\wm_icon.ico" 0 SW_SHOWNORMAL
                CreateShortCut  "$SMPROGRAMS\$StartMenuFolder\MetaGETA Shell.lnk" "$INSTDIR\metageta\metageta-shell.bat" "" "$SYSDIR\cmd.exe" 0 SW_SHOWNORMAL
                CreateShortCut  "$SMPROGRAMS\$StartMenuFolder\${APP_NAME} API Documentation.lnk" "$INSTDIR\${APP_NAME}\doc\index.html" "" "$SYSDIR\SHELL32.dll" 23 SW_SHOWMAXIMIZED
                CreateShortCut  "$SMPROGRAMS\$StartMenuFolder\Uninstall ${APP_NAME}.lnk" "$INSTDIR\uninstall.exe"
                WriteIniStr "$INSTDIR\${APP_NAME} website.url" "InternetShortcut" "URL" "${WEB_SITE}"
                CreateShortCut "$SMPROGRAMS\$StartMenuFolder\${APP_NAME} Website.lnk" "$INSTDIR\${APP_NAME} website.url" "" "$SYSDIR\SHELL32.dll" 13 SW_SHOWMAXIMIZED
            !insertmacro MUI_STARTMENU_WRITE_END
        !endif

        WriteRegStr ${REG_ROOT} "${INSTALL_PATH}"  "InstallPath" "$INSTDIR"

        WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayName" "${APP_NAME}"
        WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "UninstallString" "$INSTDIR\uninstall.exe"
        WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayIcon" "$INSTDIR\${APP_NAME}\lib\wm_icon.ico"
        WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayVersion" "${DISPLAY_VERSION}"
        WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "Publisher" "${COMP_NAME}"
        WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "URLInfoAbout" "${WEB_SITE}"
    SectionEnd

    ######################################################################

    Section Uninstall
        RMDir /r "$INSTDIR"
        !ifdef REG_START_MENU
            !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
            RMDir /r "$SMPROGRAMS\$StartMenuFolder"
        !endif
        DeleteRegKey ${REG_ROOT} "${UNINSTALL_PATH}"
        DeleteRegKey ${REG_ROOT} "${INSTALL_PATH}"
    SectionEnd

    ######################################################################

    ;Installer Functions
    Function .onInit
      !insertmacro MULTIUSER_INIT
    FunctionEnd

    ;Uninstaller Functions
    Function un.onInit
      !insertmacro MULTIUSER_UNINIT
    FunctionEnd

    Function UninstallPrevious
        ; Check for uninstaller.
        ReadRegStr $R0 ${REG_ROOT} "${UNINSTALL_PATH}" "UninstallString"
        ${If} $R0 != ""
            DetailPrint "Removing previous installation."
            messageBox MB_OK "Removing previous installation."
            ; Run the uninstaller silently.
            ExecWait '"$R0 /S"'
        ${EndIf}
    FunctionEnd
