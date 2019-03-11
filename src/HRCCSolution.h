
#include "stadfx.h"
#include "Human.h"
#include "Robot.h"

template<typename T>
bool writeDebug(std::ofstream &deg, string const &str, vector<T> const &v_val) {
	deg << str;
	for (auto & it : v_val)
	{
		deg << " " << it;
	}
	deg << endl;
	return false;
};

template<typename T>
bool writeDebug(std::ofstream &deg, string const &str, T const &v_val)
{
	deg << str;
	deg << " " << v_val << endl;
	return false;
}

class HRCCSolution
{
public:
	HRCCSolution(vector<Robot> vRob, vector<Human> vHum) {
		this->_m_vRob = vRob;
		this->_m_vHum = vHum;
		c_deg.open("D:\\VScode\\HumanRobotCommandControl\\data\\HRCC.dat");
		writeDebug(c_deg, "robNum", this->_m_vRob.size());
		writeDebug(c_deg, "humNum", this->_m_vHum.size());
	}
	~HRCCSolution();
	vector<Robot> _m_vRob;
	vector<Human> _m_vHum;
	void init();
	vector<size_t> allocate();
	pair<size_t,size_t> tempAllocate(size_t const & robID, size_t const &taskType);
	vector<size_t> _m_curCCRelation;

	vector<size_t> findFreeHuman();
	vector<size_t> findFreeRobot();

	std::ofstream c_deg;
private:
	// cMode = control mode
	// tType = task type 
	double calIncreFitness(size_t const & robID, size_t const& humID, size_t const &cMode, size_t const &tType);
	void update(size_t const & humID, size_t const & robID, size_t const &cMode, size_t const &tType);
	void eliminate(size_t const & humID, size_t const & robID, size_t const &cMode, size_t const &tType);
};

