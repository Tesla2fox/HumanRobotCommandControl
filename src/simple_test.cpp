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
	
	for (size_t i = 0; i < read_cfg._robotNum; i++)
	{
		auto resSol  = sol.tempAllocate(i, Aggregation);
		cout << " humID =  " << resSol.first;
		if (resSol.second = controlMode::MBC)
		{
			cout << " MBC " << endl;
			
		}
		else
		{
			cout << "  MBE  " << endl;
		}
	}
	
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