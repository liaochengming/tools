package com.kunyan.scalautil.message

import org.scalatest.{FlatSpec, Matchers}

/**
  * Created by yangshuai on 2014/1/1.
  */
class TextSenderTest extends FlatSpec with Matchers {

  it should "send text" in {
    TextSender.send("66", "HY_KunYanData", "98349823984", "18600397635", "test", "test")
  }
}
