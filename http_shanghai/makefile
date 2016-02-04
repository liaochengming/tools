# 指令编译器和选项  
CC=g++
CFLAGS=-Wall -std=gnu99  
  
# 目标文件  
run = main

include_path = -I./src\
	-I./library/public

SRC_PTAH = ./src
LIB_PATH = ./library/public

objects = main.o  json_data.o json_reader.o json_value.o json_writer.o hmac_sha1.o sha1.o

$(run):$(objects)
	g++ -o  $@  $^ 

main.o:
	g++ -c $(include_path) main.cpp

json_data.o:
	$(CC)  -c $(include_path) ./src/json_data.cpp

sha1.o:
	$(CC)  -c $(include_path) ./src/sha1.cpp

hmac_sha1.o:
	$(CC)  -c $(include_path) ./src/hmac_sha1.cpp

json_reader.o:
	$(CC)  -c $(include_path) ./library/public/json/json_reader.cpp

json_value.o:
	$(CC)  -c $(include_path) $(LIB_PATH)/json/json_value.cpp

json_writer.o:
	$(CC)  -c $(include_path) $(LIB_PATH)/json/json_writer.cpp

mv:
	mv  ./*.o  ./objectFile

clean:
	rm -rf *.o

