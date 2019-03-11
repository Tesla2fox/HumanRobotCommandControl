#pragma once
#include "stadfx.h"
class Robot
{
public:
	Robot();
	~Robot();
	size_t taskType;
	// if m_allianceID = - 1 means there is no alliance.	
	int m_allianceID;
	int humanID;
	size_t aggregationBool;
	size_t aggregationMBC;
	size_t aggregationMBE;
private:
	size_t nothing;
};


