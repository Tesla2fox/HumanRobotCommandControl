


#添加文件
set(file_list 
	simple_test.cpp
	Human.h Human.cpp
	Robot.h Robot.cpp
	HRCCSolution.h HRCCSolution.cpp
	stadfx.h
	ssconfig.hpp
	ReadCfg.h ReadCfg.cpp)
	
	

include_directories(../include)
find_package(Boost 1.65.0)

if(Boost_FOUND)


include_directories(${Boost_INCLUDE_DIRS})

message(${Boost_INCLUDE_DIRS})

endif()


#输出包含文件信息
message(${file_list})
message(${PROJECT_BINARY_DIR})
#message(${PROJECT_LIB_DIR})

add_executable(test_HRCC  ${file_list})
