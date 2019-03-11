#pragma once
#include "stadfx.h"
class  Human
{
public:
	Human();
	~Human();
	size_t maxWorkLoad;
	size_t curWorkLoad;
	size_t ID;
	size_t _m_controlMode;
	//vector<size_t> _m_vControlRobID;
	vector<pair<size_t, size_t>> _m_vControlRobID;
private:
	size_t nothing;
};

