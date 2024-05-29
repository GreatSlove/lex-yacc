cmake_minimum_required(VERSION 3.10)
project(MyYacc)

set(CMAKE_CXX_STANDARD 11)

add_executable(MyYacc main.cpp helper.h First.h CFGToLRDFA.h Parse_Yacc.h)