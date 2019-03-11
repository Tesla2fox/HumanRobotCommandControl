#pragma once
#include <vector>
#include <iostream>
#include <sstream>
#include <list>
#include <tuple>
#include <fstream>
#include <map>
#include <set>
#include <random>
#include <time.h>
#include <functional>
#include <algorithm>
#include <utility>
#include <memory>
#include <assert.h>
#include <limits>
#include <float.h>
#include <array>
#include <queue>

#define M_MAX std::numeric_limits<double>::max()
#define M_INF std::numeric_limits<double>::infinity()

using std::vector;
using std::string;
using std::cout;
using std::endl;
using std::list;
using std::tuple;
using std::get;
using std::shared_ptr;
using std::make_shared;
using std::map;
using std::set;
using std::pair;
using std::queue;


enum controlMode
{
	MBC = 1,
	MBE = 2,
	noControl = 3
};

enum taskMode
{
	FireGuidance = 1,
	FireAttack = 2,
	Aggregation = 3,
	Surveillance = 4,
	Search = 5
};


enum RobotType
{
	ReconnaissanceRobot = 1,
	FireAttackRobot = 2,
	MissileLauncher = 3
};

