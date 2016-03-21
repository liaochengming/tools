package com.kunyan.scalautil.net


/**
  * Created by yangshuai on 2016/3/11.
  * URL相关工具类
  */
object UrlUtil {

  /**
    * 提取url中"http(s)://xxx.xxx.xxx/"部分
    * @param url 原始url字符串
    * @return 提取结果,如果url非法则返回空字符串
    */
  def getHost(url: String): String = {

    if (!url.startsWith("http://") && !url.startsWith("https://"))
      return ""

    val arr = url.split("://")
    if (arr.length < 2)
      return ""

    arr(0) + "://" + arr(1).split("/")(0)
  }

  /**
    * 获取域名
    * @param url 原始url http://news.163.com/16/0321/10/BIM51O1I000156PO.html
    * @return 提取结果 163.com
    */
  def getDomainName(url: String): String = {

    var domain = url
    if (url.startsWith("http")) {
      try {
        domain = getHost(url)
      } catch {
        case e: Exception =>
          e.printStackTrace()
          return domain
      }
    }

    if (domain == null)
      return domain

    if (domain.startsWith("www."))
      return domain.substring(4)

    val arr = domain.split("\\.")
    if (arr.length == 4) {
      val index = domain.indexOf(".")
      return domain.substring(index + 1)
    }

    if (arr.length == 2)
      return domain

    if (arr.length == 3) {
      if (arr(2) == "cn" && (arr(1) == "net" || arr(1) == "com" || arr(1) == "org" || arr(1) == "gov")) {
        return domain
      } else {
        val index = domain.indexOf(".")
        return domain.substring(index + 1)
      }
    }

    s"strange url: $domain"
  }

}
