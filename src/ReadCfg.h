#pragma once
#include "stadfx.h"

class ReadCfg
{
public:
	ReadCfg(const char *filename) :
		_m_fileName(filename)
	{}
	~ReadCfg();
	size_t  _humanNum;
	size_t  _robotNum;
	vector<size_t> _vHumanMaxWorkload;
	vector<size_t> _vAggregationBool;
	vector<size_t> _vAggregationMBC;
	vector<size_t> _vAggregationMBE;
	vector<size_t> _vRobType;	
	void read();
private:
	const char *_m_fileName;
};

