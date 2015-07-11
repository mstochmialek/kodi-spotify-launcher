# Spotify simple launcher

import os
import sys
import subprocess
import time
import shutil
import stat
import xbmc
import xbmcaddon
import xbmcgui


addon = xbmcaddon.Addon(id='script.spotify.simplelauncher')
addonPath = addon.getAddonInfo('path')
addonIcon = addon.getAddonInfo('icon')
dialog = xbmcgui.Dialog()
language = addon.getLocalizedString
scriptid = 'script.spotify.simplelauncher'

spotifyLinux = addon.getSetting("SpotifyLinux")
spotifyWin = addon.getSetting("SpotifyWin")
spotifyOsx = addon.getSetting("SpotifyOsx")
busyDialogTime = int(addon.getSetting("BusyDialogTime"))

osWin = xbmc.getCondVisibility('system.platform.windows')
osOsx = xbmc.getCondVisibility('system.platform.osx')
osLinux = xbmc.getCondVisibility('system.platform.linux')
osAndroid = xbmc.getCondVisibility('system.platform.android')

def log(msg):
	xbmc.log(u'%s: %s' % (scriptid, msg))


def programFileExists(spotifyExe):
	if osWin + osLinux:
		return os.path.isfile(spotifyExe)
	if osOsx:
		return os.path.isdir(spotifyExe)

def spotifyExe():
	if osWin:
		return spotifyWin
	elif osOsx:
		return spotifyOsx
	elif osLinux:
		return spotifyLinux

def fileChecker():
	executable = os.path.join(spotifyExe())
	log('running program file check: %s' % executable)
	if programFileExists(executable):
		log('Spotify exists %s' % executable)
	else:
		fileCheckDialog(executable)


def fileCheckDialog(programExe):
	log('ERROR: dialog to go to addon settings because executable does not exist: %s' % programExe)
	if dialog.yesno(language(50123), programExe, language(50120), language(50121)):
		log('yes selected, opening addon settings')
		addon.openSettings()
		fileChecker()
		sys.exit()
	else:
		log('ERROR: no selected with invalid executable, exiting: %s' % programExe)
		sys.exit()




def kodiBusyDialog():
	xbmc.executebuiltin("ActivateWindow(busydialog)")
	log('busy dialog started')
	time.sleep(busyDialogTime)
	xbmc.executebuiltin("Dialog.Close(busydialog)")
	log('busy dialog stopped after: %s seconds' % busyDialogTime)


def launchSpotify():
	cmd = spotifyExe()
	try:
		log('attempting to launch: %s' % cmd)
		subprocess.Popen(cmd, shell=True, close_fds=True)
		kodiBusyDialog()
	except:
		log('ERROR: failed to launch: %s' % cmd)
		dialog.notification(language(50123), language(50126), addonIcon, 5000)


log('****Running Spotify Simple Launcher....')

if osAndroid: #osAndroid returns linux + android
	osLinux = 0

log('running on osAndroid, osOsx, osLinux, osWin: %s %s %s %s ' % (osAndroid, osOsx, osLinux, osWin))

fileChecker()
launchSpotify()