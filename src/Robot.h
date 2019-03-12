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

	size_t _m_controlMode;
	int humanID;
	size_t aggregationBool;
	size_t aggregationMBC;
	size_t aggregationMBE;
	double aggregationMBCDur;
	double aggregationMBEDur;


	size_t surveillanceBool;
	size_t surveillanceMBC;
	size_t surveillanceMBE;
	double surveillanceMBCDur;
	double surveillanceMBEDur;


private:
	size_t nothing;
};


