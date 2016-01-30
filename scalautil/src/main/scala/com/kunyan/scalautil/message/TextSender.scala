package com.kunyan.scalautil.message

import scala.io.Source

/**
  * Created by yangshuai on 2014/1/1.
  */
object TextSender {

  def send(id: String, account: String, password: String, mobile: String, keyword: String, content: String): Unit = {
    val newContent = String.format("【%s】%s", keyword, content)
    val url = String.format("http://115.29.49.158:8888/sms.aspx?action=send&userid=%s&account=%s&password=%s&mobile=%s&content=%s", id, account, password, mobile, newContent)
    Source.fromURL(url)
  }

}
