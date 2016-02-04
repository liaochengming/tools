/*
*
*  Created on: 2016.1.30
*      Author: chen
*/

#ifndef JSON_DATA_H_INCLUDED
#define JSON_DATA_H_INCLUDED

#include <iostream>
#include <fstream>
#include "json/json.h"

void get_json_file(const std::string &url, const std::string &file_name);

Json::Value get_json_array(const std::string &file_name);

std::string get_toKen(const std::string &url, const std::string &file_name);

std::vector<std::string> get_url_bytoKen(const std::string &toKen);
std::string int2str(const int &int_temp);

#endif // JSON_DATA_H