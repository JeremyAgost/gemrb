# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#


# GUIPR.py - scripts to control priest spells windows from GUIPR winpack

###################################################

import GemRB
import GUICommonWindows
from GUIDefines import *
from ie_stats import *
from GUICommon import CloseOtherWindow
#from GUICommon import ClassSkillsTable
from GUICommonWindows import *

PriestWindow = None
PriestSpellInfoWindow = None
PriestSpellLevel = 0
PriestSpellUnmemorizeWindow = None
OldOptionsWindow = None


def OpenPriestWindow ():
	global PriestWindow, OptionsWindow
	global OldOptionsWindow


	if CloseOtherWindow (OpenPriestWindow):
		if PriestWindow:
			PriestWindow.Unload ()
		if OptionsWindow:
			OptionsWindow.Unload ()
		PriestWindow = None
		GemRB.SetVar ("OtherWindow", -1)
		GemRB.SetVisible (0,1)
		GemRB.UnhideGUI ()
		OptionsWindow = OldOptionsWindow
		OldOptionsWindow = None
		SetSelectionChangeHandler(None)
		return

	GemRB.HideGUI ()
	GemRB.SetVisible (0,0)
	
	GemRB.LoadWindowPack ("GUIPR")
	PriestWindow = Window = GemRB.LoadWindowObject (2)
	GemRB.SetVar ("OtherWindow", PriestWindow.ID)
	OldOptionsWindow = GUICommonWindows.OptionsWindow
	OptionsWindow = GemRB.LoadWindowObject (0)
	SetupMenuWindowControls (OptionsWindow, 0, "OpenPriestWindow")
	OptionsWindow.SetFrame ()

	Button = Window.GetControl (1)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "PriestPrevLevelPress")

	Button = Window.GetControl (2)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "PriestNextLevelPress")

## 	#setup level buttons
## 	for i in range (7):
## 		Button = Window.GetControl (55 + i)
## 		Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "RefreshPriestLevel")
## 		Button.SetFlags (IE_GUI_BUTTON_RADIOBUTTON, OP_OR)

## 	for i in range (7):
## 		Button = Window.GetControl (55 + i)
## 		Button.SetVarAssoc ("PriestSpellLevel", i)

	# Setup memorized spells buttons
	for i in range (12):
		Button = Window.GetControl (3 + i)
		Button.SetBorder (0,0,0,0,0,0,0,0,64,0,1)
		Button.SetSprites ("SPELFRAM",0,0,0,0,0)
		Button.SetFlags (IE_GUI_BUTTON_PICTURE, OP_OR)
		Button.SetState (IE_GUI_BUTTON_LOCKED)

	# Setup book spells buttons
	for i in range (20):
		Button = Window.GetControl (27 + i)
		Button.SetFlags (IE_GUI_BUTTON_NO_IMAGE, OP_OR)
		Button.SetState (IE_GUI_BUTTON_LOCKED)

	SetSelectionChangeHandler (UpdatePriestWindow)
	UpdatePriestWindow ()

	OptionsWindow.SetVisible (1)
	Window.SetVisible (3)
	GUICommonWindows.PortraitWindow.SetVisible (1)
	return


def UpdatePriestWindow ():
	global PriestMemorizedSpellList, PriestKnownSpellList

	PriestMemorizedSpellList = []
	PriestKnownSpellList = []

	Window = PriestWindow
	pc = GemRB.GameGetSelectedPCSingle ()
	Type = IE_SPELL_TYPE_PRIEST
	level = PriestSpellLevel
	max_mem_cnt = GemRB.GetMemorizableSpellsCount (pc, Type, level)

	Label = Window.GetControl (0x10000032)
	GemRB.SetToken ('LEVEL', str (level + 1))
	Label.SetText (12137)

	Name = GemRB.GetPlayerName (pc, 0)
	Label = Window.GetControl (0x10000035)
	Label.SetText (Name)

	mem_cnt = GemRB.GetMemorizedSpellsCount (pc, Type, level)
	for i in range (12):
		Button = Window.GetControl (3 + i)
		if i < mem_cnt:
			ms = GemRB.GetMemorizedSpell (pc, Type, level, i)
			Button.SetSpellIcon (ms['SpellResRef'])
			Button.SetFlags (IE_GUI_BUTTON_NO_IMAGE, OP_NAND)
			Button.SetFlags (IE_GUI_BUTTON_PICTURE, OP_OR)
			if ms['Flags']:
				Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "OpenPriestSpellUnmemorizeWindow")
			else:
				Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "OnPriestUnmemorizeSpell")
			Button.SetEvent (IE_GUI_BUTTON_ON_RIGHT_PRESS, "OpenPriestSpellInfoWindow")
			spell = GemRB.GetSpell (ms['SpellResRef'])
			Button.SetTooltip (spell['SpellName'])
			PriestMemorizedSpellList.append (ms['SpellResRef'])
			Button.SetVarAssoc ("SpellButton", i)
			Button.EnableBorder (0, ms['Flags'] == 0)
		else:
			if i < max_mem_cnt:
				Button.SetFlags (IE_GUI_BUTTON_NORMAL, OP_SET)
			else:
				Button.SetFlags (IE_GUI_BUTTON_NO_IMAGE, OP_SET)
			Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "")
			Button.SetEvent (IE_GUI_BUTTON_ON_RIGHT_PRESS, "")
			Button.SetTooltip ('')
			Button.EnableBorder (0, 0)


	known_cnt = GemRB.GetKnownSpellsCount (pc, Type, level)
	for i in range (20):
		Button = Window.GetControl (27 + i)
		if i < known_cnt:
			ks = GemRB.GetKnownSpell (pc, Type, level, i)
			Button.SetSpellIcon (ks['SpellResRef'])
			Button.SetFlags (IE_GUI_BUTTON_NO_IMAGE, OP_NAND)
			Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "OnPriestMemorizeSpell")
			Button.SetEvent (IE_GUI_BUTTON_ON_RIGHT_PRESS, "OpenPriestSpellInfoWindow")
			spell = GemRB.GetSpell (ks['SpellResRef'])
			Button.SetTooltip (spell['SpellName'])
			PriestKnownSpellList.append (ks['SpellResRef'])
			Button.SetVarAssoc ("SpellButton", 100 + i)

		else:
			Button.SetFlags (IE_GUI_BUTTON_NO_IMAGE, OP_OR)
			Button.SetFlags (IE_GUI_BUTTON_PICTURE, OP_NAND)
			Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "")
			Button.SetEvent (IE_GUI_BUTTON_ON_RIGHT_PRESS, "")
			Button.SetTooltip ('')
			Button.EnableBorder (0, 0)

	if (ClassSkillsTable.GetValue (GemRB.GetPlayerStat( GemRB.GameGetSelectedPCSingle(), IE_CLASS), 1)=="*"):
		Window.SetVisible (2)
	else:
		Window.SetVisible (1)
	return

def PriestPrevLevelPress ():
	global PriestSpellLevel

	if PriestSpellLevel > 0:
		PriestSpellLevel = PriestSpellLevel - 1
		UpdatePriestWindow ()
	return

def PriestNextLevelPress ():
	global PriestSpellLevel

	if PriestSpellLevel < 6:
		PriestSpellLevel = PriestSpellLevel + 1
		UpdatePriestWindow ()
	return

def RefreshPriestLevel ():
	global PriestSpellLevel

	PriestSpellLevel = GemRB.GetVar ("PriestSpellLevel")
	UpdatePriestWindow ()
	return

def OpenPriestSpellInfoWindow ():
	global PriestSpellInfoWindow

	if PriestSpellInfoWindow != None:
		if PriestSpellInfoWindow:
			PriestSpellInfoWindow.Unload ()
		PriestSpellInfoWindow = None
		return

	PriestSpellInfoWindow = Window = GemRB.LoadWindowObject (3)

	#back
	Button = Window.GetControl (5)
	Button.SetText (15416)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "OpenPriestSpellInfoWindow")

	index = GemRB.GetVar ("SpellButton")
	if index < 100:
		ResRef = PriestMemorizedSpellList[index]
	else:
		ResRef = PriestKnownSpellList[index - 100]

	spell = GemRB.GetSpell (ResRef)

	#Label = Window.GetControl (0x0fffffff)
	#Label.SetText (spell['SpellName'])

	Label = Window.GetControl (0x10000000)
	Label.SetText (spell['SpellName'])

	Button = Window.GetControl (2)
	Button.SetSpellIcon (ResRef)

	Text = Window.GetControl (3)
	Text.SetText (spell['SpellDesc'])

	Window.ShowModal (MODAL_SHADOW_GRAY)
	return

def OnPriestMemorizeSpell ():
	pc = GemRB.GameGetSelectedPCSingle ()
	level = PriestSpellLevel
	Type = IE_SPELL_TYPE_PRIEST

	index = GemRB.GetVar ("SpellButton") - 100

	if GemRB.MemorizeSpell (pc, Type, level, index):
		UpdatePriestWindow ()
	return

def OpenPriestSpellRemoveWindow ():
	global PriestSpellUnmemorizeWindow

	PriestSpellUnmemorizeWindow = Window = GemRB.LoadWindowObject (5)

	# "Are you sure you want to ....?"
	TextArea = Window.GetControl (3)
	TextArea.SetText (11824)

	# Remove
	Button = Window.GetControl (0)
	Button.SetText (17507)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "OnPriestRemoveSpell")
	Button.SetFlags (IE_GUI_BUTTON_DEFAULT, OP_OR)

	# Cancel
	Button = Window.GetControl (1)
	Button.SetText (13727)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "OpenPriestSpellRemoveWindow")
	Button.SetFlags (IE_GUI_BUTTON_CANCEL, OP_OR)

	Window.ShowModal (MODAL_SHADOW_GRAY)
	return

def ClosePriestSpellUnmemorizeWindow ():
	global PriestSpellUnmemorizeWindow

	if PriestSpellUnmemorizeWindow:
		PriestSpellUnmemorizeWindow.Unload ()
	PriestSpellUnmemorizeWindow = None
	return

def OpenPriestSpellUnmemorizeWindow ():
	global PriestSpellUnmemorizeWindow

	PriestSpellUnmemorizeWindow = Window = GemRB.LoadWindowObject (5)

	# "Are you sure you want to ....?"
	TextArea = Window.GetControl (3)
	TextArea.SetText (11824)

	# Remove
	Button = Window.GetControl (0)
	Button.SetText (17507)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "OnPriestUnmemorizeSpell")
	Button.SetFlags (IE_GUI_BUTTON_DEFAULT, OP_OR)

	# Cancel
	Button = Window.GetControl (1)
	Button.SetText (13727)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "ClosePriestSpellUnmemorizeWindow")
	Button.SetFlags (IE_GUI_BUTTON_CANCEL, OP_OR)

	Window.ShowModal (MODAL_SHADOW_GRAY)
	return

def OnPriestUnmemorizeSpell ():
	if PriestSpellUnmemorizeWindow:
		ClosePriestSpellUnmemorizeWindow ()

	pc = GemRB.GameGetSelectedPCSingle ()
	level = PriestSpellLevel
	Type = IE_SPELL_TYPE_PRIEST

	index = GemRB.GetVar ("SpellButton")

	if GemRB.UnmemorizeSpell (pc, Type, level, index):
		UpdatePriestWindow ()
	return

def OnPriestRemoveSpell ():
	ClosePriestSpellUnmemorizeWindow()
	OpenPriestSpellInfoWindow()

	pc = GemRB.GameGetSelectedPCSingle ()
	level = PriestSpellLevel
	Type = IE_SPELL_TYPE_PRIEST

	index = GemRB.GetVar ("SpellButton")-100

	#remove spell from memory
	GemRB.RemoveSpell (pc, Type, level, index)
	UpdatePriestWindow ()
	return

###################################################
# End of file GUIPR.py
