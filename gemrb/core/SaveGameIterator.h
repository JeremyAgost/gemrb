/* GemRB - Infinity Engine Emulator
 * Copyright (C) 2003 The GemRB Project
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.

 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 *
 */

#ifndef SAVEGAMEITERATOR_H
#define SAVEGAMEITERATOR_H

#include <time.h>
#include <sys/stat.h>
#include <list> 
#include "exports.h"
#include "FileStream.h"
#include "ResourceManager.h"

#define SAVEGAME_DIRECTORY_MATCHER "%d - %[A-Za-z0-9- _]"

class ImageMgr;

class GEM_EXPORT SaveGame {
public:
	SaveGame(char* path, char* name, char* prefix, int pCount, int saveID);
	~SaveGame();
	int GetPortraitCount()
	{
		return PortraitCount;
	}
	int GetSaveID()
	{
		return SaveID;
	}
	const char* GetName()
	{
		return Name;
	}
	const char* GetPrefix()
	{
		return Prefix;
	}
	const char* GetPath()
	{
		return Path;
	}
	const char* GetDate()
	{
		return Date;
	}

	Sprite2D* GetPortrait(int index);
	Sprite2D* GetScreen();
	DataStream* GetGame();
	DataStream* GetWmap();
	DataStream* GetSave();
private:
	char Path[_MAX_PATH];
	char Prefix[10];
	char Name[_MAX_PATH];
	char Date[_MAX_PATH];
	int PortraitCount;
	int SaveID;
	ResourceManager manager;
};

typedef std::list<char *> charlist;

class GEM_EXPORT SaveGameIterator {
private:
	bool loaded;
	charlist save_slots;

public:
	SaveGameIterator(void);
	~SaveGameIterator(void);
	void Invalidate();
	bool RescanSaveGames();
	int GetSaveGameCount();
	SaveGame* GetSaveGame(int index);
	void DeleteSaveGame(int index);
	int ExistingSlotName(int index);
	int CreateSaveGame(int index, const char *slotname, bool mqs = false);
private:
	char *GetSaveName(int index);
	void PruneQuickSave(const char *folder);
};

#endif