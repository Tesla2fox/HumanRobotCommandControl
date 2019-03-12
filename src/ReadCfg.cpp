#include "ReadCfg.h"
#include "ssconfig.hpp"




ReadCfg::~ReadCfg()
{
}

void ReadCfg::read()
{
	sscfg::ConfigFile co_list = sscfg::ConfigFile::load(_m_fileName);
	co_list.get("humanNum", _humanNum);
	co_list.get("robotNum", _robotNum);
	co_list.get("humanMaxWorkload", _vHumanMaxWorkload);
	co_list.get("aggregationBool", _vAggregationBool);
	co_list.get("aggregationMBC", _vAggregationMBC);
	co_list.get("aggregationMBE", _vAggregationMBE);
	co_list.get("aggregationMBCDur", _vAggregationMBCdur);
	co_list.get("aggregationMBEDur", _vAggregationMBEdur);

	co_list.get("surveillanceBool", _vSurveillanceBool);
	co_list.get("surveillanceMBC", _vSurveillanceMBC);
	co_list.get("surveillanceMBE", _vSurveillanceMBE);
	co_list.get("surveillanceMBCDur", _vSurveillanceMBCdur);
	co_list.get("surveillanceMBEDur", _vSurveillanceMBEdur);


	co_list.get("robType", _vRobType);
}
