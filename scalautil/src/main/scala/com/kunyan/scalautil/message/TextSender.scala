package com.kunyan.scalautil.message

import scala.io.Source

/**
  * Created by yangshuai on 2016/1/30.
  */
object TextSender {

  /**
    * 发送短信,短信内容的格式为"${content}【${key}】"
    * id,account,password向组长索取
    *
    * @param id id
    * @param account 账号
    * @param password 密码
    * @param mobile 电话号码
    * @param keyword "【】"中的内容
    * @param content "【】"前的正文
    */
  def send(id: String, account: String, password: String, mobile: String, keyword: String, content: String): Unit = {
    val newContent = String.format("【%s】%s", keyword, content)
    val url = String.format("http://115.29.49.158:8888/sms.aspx?action=send&userid=%s&account=%s&password=%s&mobile=%s&content=%s", id, account, password, mobile, newContent)
    Source.fromURL(url)
  }

}
