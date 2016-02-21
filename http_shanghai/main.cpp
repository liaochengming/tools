#include <iostream>

#include"my_include.h"

using namespace std;

int main(int argc, char* argv[])
{
	std::string password = "kunyan123";
	std::string md5_code = get_md5(password);
	std::cout << md5_code << std::endl;

	std::string apikey = "e_kunyan98f5103019170612fd3a486e3d872c48";
	std::string sign = get_hmac_sha1(md5_code, apikey);
	std::cout << sign << std::endl;

	std::string url = "http://61.129.39.71/telecom-dmp/getToken?apiKey=98f5103019170612fd3a486e3d872c48&sign=6a653929c81a24ba14e41e25b6047e5dec55e76e";
	std::string toke_file = "token_file";
	std::string token = (get_toKen(url, toke_file));
	std::cout << token << std::endl;

	std::vector<std::string> url_2 = get_url_bytoKen(token);
	//std::cout << url_2 << std::endl;

	for (int i = 0; i < 500; i++)
	{

		std::string value_file = "value_file";
		get_json_file(url_2[i], value_file);
		std::cout << get_json_array(value_file);

	}
}


