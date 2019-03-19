#include "HRCCSolution.h"



HRCCSolution::~HRCCSolution()
{
}

void HRCCSolution::init()
{
	this->_m_curCCRelation.assign(this->_m_vRob.size(), -1);
}

vector<size_t> HRCCSolution::allocate()
{
	auto freeHuman = this->findFreeHuman();
	auto freeRob = this->findFreeRobot();


	if (freeHuman.size() == this->_m_vHum.size() && freeRob.size() == this->_m_vRob.size())
	{
		cout << "init allocation" << endl;
		//作战小组与指挥员的关系如何确定
		//计算每个作战小组
		cout << " humSize = " << this->_m_vHum.size() << endl;
		for (size_t i = 0; i < this->_m_vRob.size(); i++)
		{
			this->_m_curCCRelation[i] =
				this->_m_vRob[i].m_allianceID;
			cout << _m_vRob[i].m_allianceID << " __";
		}
	}
	else
	{
		cout << "during allocation" << endl;
	}
	for (size_t i = 0; i < this->_m_vRob.size(); i++)
	{
		this->_m_vRob[i].humanID = this->_m_curCCRelation[i];
	}
	writeDebug(this->c_deg, "alliance", this->_m_curCCRelation);
	return this->_m_curCCRelation;
}

pair<size_t, size_t> HRCCSolution::tempAllocate(size_t const & robID, size_t const & taskType, double  const &arrTime)
{
	auto &  rob = this->_m_vRob[robID];
	auto compTuple = [](tuple<size_t, size_t, double> & a, tuple<size_t, size_t, double> b)
	{
		return get<2>(a) < get<2>(b);
	};
	switch (taskType)
	{
	case Aggregation:
	case Surveillance:
	{
		vector<tuple<size_t, size_t, double>> vFitness;
		for (size_t i = 0; i < _m_vHum.size(); i++)
		{
			double  MBCFitness = this->calIncreFitness(robID, i, controlMode::MBC, taskType, arrTime);
			vFitness.push_back(tuple<size_t, size_t, double>(i, controlMode::MBC, MBCFitness));
			if (taskType == Aggregation)
			{
				if (rob.aggregationBool == 1)
				{
					double  MBEFitness = this->calIncreFitness(robID, i, controlMode::MBE, taskType, arrTime);
					vFitness.push_back(tuple<size_t, size_t, double>(i, controlMode::MBE, MBEFitness));
				}
			}
			if (taskType == Surveillance)
			{
				if (rob.surveillanceBool== 1)
				{
					double  MBEFitness = this->calIncreFitness(robID, i, controlMode::MBE, taskType, arrTime);
					vFitness.push_back(tuple<size_t, size_t, double>(i, controlMode::MBE, MBEFitness));
				}
			}
		}
		std::sort(vFitness.begin(), vFitness.end(), compTuple);
		auto &maxFitness = vFitness.back();
		pair<size_t, size_t> res;
		res.first = get<0>(maxFitness);
		res.second = get<1>(maxFitness);
		this->update(res.first, robID, res.second, taskType, arrTime);
		return res;
		break;
	}
	default:
		break;
	}
	return pair<size_t, size_t>(1, 1);
}

vector<size_t> HRCCSolution::findFreeHuman()
{
	vector<size_t> freeHum;
	for (size_t i = 0; i < this->_m_vHum.size(); i++)
	{
		if (_m_vHum[i]._m_vControlRobID.empty())
			freeHum.push_back(i);
	}
	return freeHum;
}

vector<size_t> HRCCSolution::findFreeRobot()
{
	vector<size_t> freeRob;
	for (size_t i = 0; i < this->_m_vRob.size(); i++)
	{
		if (_m_vRob[i].humanID == -1)
			freeRob.push_back(i);
	}
	return freeRob;
}

void HRCCSolution::eliminate(size_t const & robID, double const & eliminateTime)
{
	auto & rob = this->_m_vRob[robID];
	eliminate(rob.humanID, robID, rob._m_controlMode, rob.taskType, eliminateTime);
}

double HRCCSolution::calIncreFitness(size_t const & robID, size_t const & humID, size_t const & cMode, size_t const & tType
	, double  const &arrTime)
{
	auto &hum = this->_m_vHum[humID];
	auto &rob = this->_m_vRob[robID];
	double increWorkLoad;
	double predictCompTime = arrTime;
	switch (tType)
	{
	case Aggregation:
	{
		if (cMode == controlMode::MBC)
		{
			increWorkLoad = rob.aggregationMBC;
			predictCompTime = rob.aggregationMBCDur;
		}
		if (cMode == controlMode::MBE)
		{
			increWorkLoad = rob.aggregationMBE;
			predictCompTime = rob.aggregationMBEDur;
		}
		for (size_t i = 0; i < hum._m_vControlRobID.size(); i++)
		{
			auto & it = hum._m_vControlRobID[i];
			if (it.second == controlMode::MBC)
				predictCompTime += this->_m_vRob[i].aggregationMBCDur;
			else
				predictCompTime += this->_m_vRob[i].aggregationMBEDur;
		}
		break;
	}
	case Surveillance:
	{
		if (cMode == controlMode::MBC)
		{
			increWorkLoad = rob.surveillanceMBC;
			predictCompTime = rob.surveillanceMBCDur;
		}
		if (cMode == controlMode::MBE)
		{
			increWorkLoad = rob.surveillanceMBE;
			predictCompTime = rob.surveillanceMBEDur;
		}
		for (size_t i = 0; i < hum._m_vControlRobID.size(); i++)
		{
			auto & it = hum._m_vControlRobID[i];
			if (it.second == controlMode::MBC)
				predictCompTime += this->_m_vRob[i].surveillanceMBCDur;
			else
				predictCompTime += this->_m_vRob[i].surveillanceMBEDur;
		}
		break;
	}
	default:
		break;
	}
	auto predictWorkLoad = hum.curWorkLoad + increWorkLoad;
	auto leftWorkLoad = hum.maxWorkLoad - predictWorkLoad;
	if (leftWorkLoad >= 0)
	{
		double trustRatio;
		if (rob.m_allianceID == humID)
			trustRatio = 2;
		else
			trustRatio = 1;
		double thresholdWorkLoad = hum.maxWorkLoad  *0.7;
		double  approWorkLoad = abs(predictWorkLoad - thresholdWorkLoad);
		if (approWorkLoad < 1)
			approWorkLoad = 1;
		return trustRatio / approWorkLoad / predictCompTime;
	}
	else
	{
		double trustRatio;
		if (rob.m_allianceID == humID)
			trustRatio = 1;
		else
			trustRatio = 2;
		return trustRatio * leftWorkLoad;
	}
	return 0.0;
}

void HRCCSolution::update(size_t const & humID, size_t const & robID, size_t const & cMode, size_t const & tType,
	double const &arrTime)
{
	auto &hum = this->_m_vHum[humID];
	auto &rob = this->_m_vRob[robID];
	double increseWorkLoad;
	switch (tType)
	{
	case Aggregation:
	{
		if (cMode == controlMode::MBC)
			increseWorkLoad = rob.aggregationMBC;
		else
			increseWorkLoad = rob.aggregationMBE;
		break;
	}
	case Surveillance:
	{
		if (cMode == controlMode::MBC)
			increseWorkLoad = rob.surveillanceMBC;
		else
			increseWorkLoad = rob.surveillanceMBE;
		break;
	}
	default:
		break;
	}
	hum.curWorkLoad += increseWorkLoad;
	hum._m_vControlRobID.push_back(pair<size_t, size_t>(robID, cMode));
	rob.taskType = tType;
	rob._m_controlMode = cMode;
	rob.humanID = humID;
	std::string robName;
	robName = "rob";
	robName += std::to_string(robID);
	//	writeDebug(this->c_deg, robName, );
	c_deg << "HumanWorkLoad " << hum.curWorkLoad << " humID " << humID
		<< " time " << arrTime << endl;
	//writeDebug(this->c_deg,"Human",)
}

void HRCCSolution::eliminate(size_t const & humID, size_t const & robID, size_t const & cMode, size_t const & tType,
	double const &eliminateTime)
{
	cout << "bug is here ?" << endl;

	auto &hum = this->_m_vHum[humID];
	auto &rob = this->_m_vRob[robID];
	double eliminateWorkLoad;
	switch (tType)
	{
	case Aggregation:
	{
		if (cMode == controlMode::MBC)
			eliminateWorkLoad = rob.aggregationMBC;
		else
			eliminateWorkLoad = rob.aggregationMBE;
		break;
	}
	case Surveillance:
	{
		if (cMode == controlMode::MBC)
			eliminateWorkLoad = rob.surveillanceMBC;
		else
			eliminateWorkLoad = rob.surveillanceMBE;
		break;
	}
	default:
		break;
	}
	hum.curWorkLoad -= eliminateWorkLoad;

	c_deg << "HumanWorkLoad " << hum.curWorkLoad << " humID " << humID
		<< " time " << eliminateTime << endl;
	//c_deg << "humIDE " << humID << " robID " << robID
	//	<< " startTime " << eliminateTime << endl;;

	decltype(hum._m_vControlRobID.begin()) eraseIt;
	//auto eraseIt = 
	for (auto it = hum._m_vControlRobID.begin(); it != hum._m_vControlRobID.end(); it++)
	{
		if (it->first == robID)
		{
			eraseIt = it;
			break;
		}
	}
	//std::find(hum._m_vControlRobID.begin(), hum._m_vControlRobID.end(), )
	hum._m_vControlRobID.erase(eraseIt);
}
