#pragma once
#include <iostream>
#include "stadfx.h"
#include <random>
#include "Robot.h"
#include "Human.h"
#include "HRCCSolution.h"
#include "ReadCfg.h"

void main()
{
	std::cout << "»¶Ó­»ØÀ´,ggq" << std::endl;


	ReadCfg read_cfg("D:\\VScode\\HumanRobotCommandControl\\data\\cfg.txt");
	read_cfg.read();
	

	vector<Robot> vRob;
	std::default_random_engine eng;
	std::uniform_int_distribution<size_t> dis(0, 3);

	for (size_t i = 0; i < read_cfg._robotNum; i++)
	{
		Robot rob;
		rob.humanID = -1;
		rob.m_allianceID = dis(eng);
		rob.aggregationBool = read_cfg._vAggregationBool[i];
		rob.aggregationMBC = read_cfg._vAggregationMBC[i];
		rob.aggregationMBE = read_cfg._vAggregationMBE[i];
		rob.aggregationMBCDur = read_cfg._vAggregationMBCdur[i];
		rob.aggregationMBEDur = read_cfg._vAggregationMBEdur[i];

		rob.surveillanceBool = read_cfg._vSurveillanceBool[i];
		rob.surveillanceMBC = read_cfg._vSurveillanceMBC[i];
		rob.surveillanceMBE = read_cfg._vSurveillanceMBE[i];
		rob.surveillanceMBCDur = read_cfg._vSurveillanceMBCdur[i];
		rob.surveillanceMBEDur = read_cfg._vSurveillanceMBEdur[i];

		vRob.push_back(rob);
	}
	vector<Human> vHum;
	for (size_t i = 0; i < read_cfg._humanNum; i++)
	{
		Human hum;
		hum.maxWorkLoad = read_cfg._vHumanMaxWorkload[i];
		hum.curWorkLoad = 0;
		hum._m_controlMode = controlMode::noControl;
		vHum.push_back(hum);
	}

	HRCCSolution sol(vRob, vHum);
	sol.init();
	auto  res =  sol.allocate();
	
	vector<double> vHumTime;
	vHumTime.assign(vRob.size(), 0);

	//std::default_random_engine eng;
	eng.seed(1);
	std::uniform_real_distribution<double> d_dis(0.8, 3);
	vector<double> vMBCTime;
	vector<double> vMBETime;
	for (size_t i = 0; i < read_cfg._robotNum; i++)
	{
		vMBCTime.push_back(d_dis(eng));
		vMBETime.push_back(d_dis(eng));
	}
	//std::uniform_int_distribution<size_t> dis(0, 3);

	vector<pair<double, size_t>> vendTime;
	for (size_t i = 0; i < read_cfg._robotNum; i++)
	{
		auto resSol  = sol.tempAllocate(i, Aggregation,0);
		cout << " humID =  " << resSol.first;
		if (resSol.second == controlMode::MBC)
		{
			double processTime = vMBCTime[i];
			//double processTime = d_dis(eng);
			sol.c_deg << "humID " << resSol.first << " robID "<< i
				<< " startTime " << vHumTime[resSol.first];
			vHumTime[resSol.first] += processTime;
			sol.c_deg << " endTime " << vHumTime[resSol.first] << endl;
			vendTime.push_back(pair<double, size_t>(vHumTime[resSol.first], i));
			cout << " MBC " << endl;
		}
		else
		{
			double processTime = vMBETime[i];
			sol.c_deg << "humID " << resSol.first << " robID " << i
				<< " startTime " << vHumTime[resSol.first];
			vHumTime[resSol.first] += processTime;
			vendTime.push_back(pair<double, size_t>(vHumTime[resSol.first], i));
			sol.c_deg << " endTime " << vHumTime[resSol.first] << endl;
			cout << " MBE " << endl;
		}
	}
	
	std::sort(vendTime.begin(), vendTime.end());
	for (size_t i = 0; i < vendTime.size(); i++)
	{
		sol.eliminate(vendTime[i].second, vendTime[i].first);
	}

	std::uniform_real_distribution<double> s_dis(3, 5);
	vector<double> _vsTimeMBC;
	//		; vsTimeMBC
	for (size_t i = 0; i < read_cfg._robotNum; i++)
	{
		_vsTimeMBC.push_back(s_dis(eng));
	}
	
	vector<double> _vsTimeArr;
	
	for (size_t i = 0; i < read_cfg._humanNum; i++)
	{
		_vsTimeArr.push_back(i + 15);
		vHumTime[i] = i + 15;
	}	

	vector<pair<double, size_t>> _vsTimeSeq;
	for (size_t i = 0; i < read_cfg._robotNum; i++)
	{
		_vsTimeSeq.push_back(pair<double, size_t>(_vsTimeArr[res[i]],i));
	}
	std::sort(_vsTimeSeq.begin(), _vsTimeSeq.end());

	
	vendTime.clear();
	for (size_t i = 0; i < read_cfg._robotNum; i++)
	{
		cout << " time " << _vsTimeSeq[i].first <<" robID "<< _vsTimeSeq[i].second
			<< endl;
		auto resSol = sol.tempAllocate(_vsTimeSeq[i].second, Surveillance,_vsTimeSeq[i].first);
		if (resSol.second == controlMode::MBC)
		{
			double processTime = _vsTimeMBC[_vsTimeSeq[i].second];
			//double processTime = d_dis(eng);
			sol.c_deg << "humID " << resSol.first << " robID " << _vsTimeSeq[i].second
				<< " startTime " << vHumTime[resSol.first];
			vHumTime[resSol.first] += processTime;
			sol.c_deg << " endTime " << vHumTime[resSol.first] << endl;
			vendTime.push_back(pair<double, size_t>(vHumTime[resSol.first], _vsTimeSeq[i].second));
			cout << " MBC " << endl;
		}
		else
		{
			double processTime = _vsTimeMBC[_vsTimeSeq[i].second];
			//double processTime = d_dis(eng);
			sol.c_deg << "humID " << resSol.first << " robID " << _vsTimeSeq[i].second
				<< " startTime " << vHumTime[resSol.first];
			vHumTime[resSol.first] += processTime;
			sol.c_deg << " endTime " << vHumTime[resSol.first] << endl;
			vendTime.push_back(pair<double, size_t>(vHumTime[resSol.first], _vsTimeSeq[i].second));
			cout << " MBE " << endl;
		}
	}
	std::sort(vendTime.begin(), vendTime.end());
	for (size_t i = 0; i < vendTime.size(); i++)
	{
		sol.eliminate(vendTime[i].second, vendTime[i].first);
	}

	//	res.push_back()
	
	for (auto &it : res)
	{	
		std::cout << it << " ";
	}	
	auto  res2 = sol.allocate();
	for (auto &it : res2)
	{
		std::cout << it << " ";
	}
	int i;
	std::cin >> i;
}