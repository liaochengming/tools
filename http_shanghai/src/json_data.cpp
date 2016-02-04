/*
*
*  Created on: 2016.1.30
*      Author: chenxun
*/
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include "json_data.h"
using namespace std;

void get_json_file(const std::string &url, const std::string &file_name)
{
	std::string  link_text = "curl \"" + url + "\"" + " -o " + file_name;
	//std::cout << link_text << std::endl;
	system(link_text.c_str());
}

Json::Value get_json_array(const std::string &file_name)
{
	std::ifstream file(file_name.c_str());
	if (!file)
	{
		std::cout << "Open file the json_dat.txt fail!!!" << std::endl;
		return 0;
	}

	Json::Value root;
	Json::Reader reader;

	if (!reader.parse(file, root, false))
	{
		std::cout << "--Plz check your url make sure your url is available--" << std::endl;
		return 0;
	}

	return root;
}

std::string get_toKen(const std::string &url, const std::string &file_name)
{
	std::string toKen = "";
	Json::Value root;

	get_json_file(url, file_name);

	root  = get_json_array(file_name);
	toKen = root["result"].asString();
	//std::cout << toKen << std::endl;
	return toKen;
}

std::string int2str(const int &int_temp)
{
	stringstream stream;
	stream << int_temp;
	std::string string_temp = stream.str();   //此处也可以用 stream>>string_temp
	return string_temp; 
}

std::vector<std::string> get_url_bytoKen(const std::string &toKen)
{
	std::vector<std::string> url_vec;
	std::string url1_ip	   = "http://61.129.39.71/telecom-dmp/kv/getValueByKey?token=";
	std::string url2_toKen = toKen;
	std::string url3_table = "table=kunyan_to_upload_inter_tab_sk";
	std::string url4_key = "key=201602021000_kunyan_";

	//std::vector<std::string> num_key;
	for (int i = 0; i < 500; i++)
	{
		//num_key.push_back(int2str(i));
		std::string url = url1_ip + url2_toKen + "&" + url3_table + "&" + url4_key + int2str(i);
		url_vec.push_back(url);
	}

	//std::cout << url << std::endl;
	return url_vec;
}

