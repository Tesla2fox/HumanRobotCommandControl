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
		for (size_t i = 0; i < this->_m_vRob.size(); i++)
		{
			this->_m_curCCRelation[i] =
				this->_m_vRob[i].m_allianceID;
			//cout << _m_vRob[i].m_allianceID << " __";
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

pair<size_t, size_t> HRCCSolution::tempAllocate(size_t const & robID, size_t const & taskType)
{
	auto &  rob = this->_m_vRob[robID];
	auto compTuple = [](tuple<size_t, size_t, double> & a, tuple<size_t, size_t, double> b)
	{
		return get<2>(a) < get<2>(b);
	};	
	switch (taskType)
	{
	case Aggregation:
	{
		vector<tuple<size_t, size_t, double>> vFitness;
		for (size_t i = 0; i < _m_vHum.size(); i++)
		{
			double  MBCFitness = this->calIncreFitness(robID, i, controlMode::MBC, Aggregation);
			vFitness.push_back(tuple<size_t, size_t, double>(i, controlMode::MBC, MBCFitness));
			if (rob.aggregationBool == 1)
			{
				double  MBEFitness = this->calIncreFitness(robID, i, controlMode::MBE, Aggregation);
				vFitness.push_back(tuple<size_t, size_t, double>(i, controlMode::MBC, MBCFitness));
			}
		}
		std::sort(vFitness.begin(), vFitness.end(), compTuple);
		auto &maxFitness = vFitness.back();
		pair<size_t, size_t> res;
		res.first = get<0>(maxFitness);
		res.second = get<1>(maxFitness);
		this->update(res.first, robID, res.second, taskType);
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

double HRCCSolution::calIncreFitness(size_t const & robID, size_t const & humID, size_t const & cMode, size_t const & tType)
{
	auto &hum = this->_m_vHum[humID];
	auto &rob = this->_m_vRob[robID];
	double increWorkLoad;
	switch (tType)
	{
	case Aggregation:
		if (cMode == controlMode::MBC)
			increWorkLoad = rob.aggregationMBC;
		if (cMode == controlMode::MBE)
			increWorkLoad = rob.aggregationMBE;
		break;
	default:
		break;
	}

	auto predictWorkLoad = hum.curWorkLoad + increWorkLoad;
	auto leftWorkLoad = hum.maxWorkLoad - predictWorkLoad;
	if (leftWorkLoad >= 0)
	{
		double trustRatio;
		if (rob.m_allianceID == humID)
			trustRatio = 3;
		else
			trustRatio = 1;
		double thresholdWorkLoad = hum.maxWorkLoad  *0.7;
		double  approWorkLoad = abs(predictWorkLoad - thresholdWorkLoad);
		return trustRatio * approWorkLoad;
	}
	else
	{
		double trustRatio;
		if (rob.m_allianceID == humID)
			trustRatio = 1;
		else
			trustRatio = 3;
		return trustRatio * leftWorkLoad;
	}
	return 0.0;
}

void HRCCSolution::update(size_t const & humID, size_t const & robID, size_t const & cMode, size_t const & tType)
{
	auto &hum = this->_m_vHum[humID];
	auto &rob = this->_m_vRob[robID];
	double increseWorkLoad;
	switch (tType)
	{
	case Aggregation:
		if (cMode == controlMode::MBC)
			increseWorkLoad = rob.aggregationMBC;
		else
			increseWorkLoad = rob.aggregationMBE;
		break;
	default:
		break;
	}
	hum.curWorkLoad += increseWorkLoad;
	hum._m_vControlRobID.push_back(pair<size_t, size_t>(robID, cMode));

}

void HRCCSolution::eliminate(size_t const & humID, size_t const & robID, size_t const & cMode, size_t const & tType)
{
	auto &hum = this->_m_vHum[humID];
	auto &rob = this->_m_vRob[robID];
	double eliminateWorkLoad;
	switch (tType)
	{
	case Aggregation:
		if (cMode == controlMode::MBC)
			eliminateWorkLoad = rob.aggregationMBC;
		else
			eliminateWorkLoad = rob.aggregationMBE;
		break;
	default:
		break;
	}
	hum.curWorkLoad -= eliminateWorkLoad;
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
