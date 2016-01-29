package com.kunyan.scalautil.hdfs

import java.io.{BufferedReader, File, InputStreamReader}

import com.google.common.base.Charsets
import com.google.common.io.Files
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FSDataOutputStream, FileSystem, Path}

import scala.collection.mutable.ListBuffer

/**
  * Created by yangshuai on 2016/1/29.
  */
object HDFSHelper {

  /**
    * 创建路径
    *
    * @param uri 例: "hdfs://server:9000"
    * @param directory 路径名
    * @return true:该路径不存在,创建成功
    *         false:该路径已存在
    */
  def mkDir(uri:String, directory:String): Boolean ={
    val conf = new Configuration()
    conf.set("fs.defaultFS", uri)
    val fs = FileSystem.get(conf)
    if(!fs.exists(new Path(uri + directory))){
      fs.mkdirs(new Path(uri + directory))
      fs.close()
      true
    }else{
      fs.close()
      false
    }
  }

  private def write(uri: String, filePath: String, data: Array[Byte], append: Boolean) = {

    val path = new Path(filePath)

    val conf = new Configuration()
    conf.set("fs.defaultFS", uri)
    conf.set("dfs.client.block.write.replace-datanode-on-failure.policy", "NEVER")
    conf.setBoolean("dfs.client.block.write.replace-datanode-on-failure.enable", true)
    conf.setBoolean("dfs.support.append", true)

    val fs = FileSystem.get(conf)
    var os:FSDataOutputStream = null

    if (append)
      os = fs.append(path)
    else
      os = fs.create(path)

    os.write(data)

    os.close()
    fs.close()
  }

  /**
    * 将字符串写入hdfs
    *
    * @param uri 例: "hdfs://server:9000"
    * @param filePath hdfs上的路径
    * @param str 要写入文件的内容
    * @param append true:追加内容,false:覆盖原有内容
    */
  def write(uri: String, filePath: String, str: String, append: Boolean):Unit = {
    write(uri, filePath, str.getBytes(), append)
  }

  /**
    * 将字符串数组中的每个字符串作为一行写入hdfs
    *
    * @param uri 例: "hdfs://server:9000"
    * @param filePath hdfs上的路径
    * @param seq 要写入文件的内容
    * @param append true:追加内容,false:覆盖原有内容
    */
  def write(uri: String, filePath: String, seq: Seq[String], append: Boolean):Unit = {
    val list = ListBuffer[Byte]()
    for (str <- seq) {
      list ++= (str + "\n").getBytes().toSeq
    }
    write(uri, filePath, list.toArray, append)
  }

  /**
    * 将文件写入hdfs,编码格式为UTF-8
    *
    * @param uri 例: "hdfs://server:9000"
    * @param filePath hdfs上的路径
    * @param file 要写入的文件
    * @param append true:追加内容,false:覆盖原有内容
    */
  def write(uri: String, filePath: String, file: File, append: Boolean): Unit = {
    write(uri, filePath, Files.toString(file, Charsets.UTF_8), append)
  }

  /**
    * 读取hdfs上的文件
    *
    * @param uri 例: "hdfs://server:9000"
    * @param filePath hdfs上的路径
    * @return
    */
  def open(uri:String, filePath:String): ListBuffer[String] = {

    val list = ListBuffer[String]()

    try{

      val conf = new Configuration()
      conf.set("fs.defaultFS", uri)
      val fs = FileSystem.get(conf)
      val in  = fs.open(new Path(filePath),4096)
      val bufferReader = new BufferedReader(new InputStreamReader(in))
      var line = bufferReader.readLine()
      while(line !=null){
        list += line
        line = bufferReader.readLine()
      }
      fs.close()

      list
    } catch {
      case e: Exception =>
        e.printStackTrace()
        ListBuffer[String]()
    }
  }

  /**
    * 删除文件或路径
    *
    * @param uri 例: "hdfs://server:9000"
    * @param filePath hdfs上的路径
    * @param recursive 是否递归删除
    */
  def delete(uri:String, filePath:String, recursive:Boolean): Unit = {
    val conf = new Configuration()
    conf.set("fs.defaultFS", uri)
    val fs = FileSystem.get(conf)
    fs.delete(new Path(filePath), recursive)
    fs.close()
  }

}
