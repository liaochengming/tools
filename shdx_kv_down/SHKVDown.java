import net.sf.json.JSONException;
import net.sf.json.JSONObject;
import org.apache.commons.codec.binary.Hex;
import sun.misc.BASE64Decoder;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.security.MessageDigest;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.logging.Logger;

/**
 * Created by liaochengming on 2015-12-14.
 *此类是用来下载上海电信kv表中的数据
 *
 *
 */
public class SHKVDown {

    private static final String HMAC_SHA1_ALGORITHM = "HmacSHA1";

    /**
     *
     * @param args
     * args[0] 指定下载的时间（分钟）1表示0-4分钟。。。
     * args[1] 指定下载的时间（小时）1表示1小时之前
     */
    public static void main(String[] args) {

        String yth = getYearToHour(Integer.valueOf(args[1]));


        try {

            //合并文件，判断保存下载文件的文件夹下是否有上个小时的文件
            //如果有就合并
            MergedFiles.doMer();

            String token = getToken();

            String fileOver;
            File writer_file;

//            fileOver = "/home/telecom/shdx/bin/shdx_kv_down/write_over.txt";
            fileOver = "F:\\write_over.txt";
            writer_file = new File(fileOver);
            BufferedWriter writer = new BufferedWriter(new FileWriter(writer_file));
            int min_start = Integer.valueOf(args[0]);
            ExecutorService cachedThreadPool = Executors.newCachedThreadPool();

            //创建4个进程，一个进程跑一分钟的数据
            for (int i = (min_start - 1) * 4; i < min_start * 4; i++) {

                cachedThreadPool.execute(new Thread(new DoGetValue(yth, getMS(i), i, token)));

            }

            cachedThreadPool.shutdown();

            while (true) {

                if (cachedThreadPool.isTerminated()) {

                    //System.out.println("结束了！");
                    String isOver = readFileByLines(fileOver);

                    if (isOver.equals("false")) {

                        writer.write("true1");

                    } else {

                        int trueNum = Integer.valueOf(isOver.substring(4));
                        trueNum = trueNum + 1;
                        writer.write("true" + trueNum);

                    }

                    writer.flush();
                    break;

                }

                Thread.sleep(2000);

            }

            writer.close();

        } catch (Exception e) {

            e.printStackTrace();

        }


    }

    /**
     * 一行行读文件
     * @param path
     * path 文件路径
     * @return 一行数据
     */
    public static String readFileByLines(String path) {

        File file = new File(path);

        if (file.exists()) {

            BufferedReader reader = null;

            try {

                reader = new BufferedReader(new FileReader(file));
                String tempString;

                // 只读一行
                tempString = reader.readLine();
                reader.close();

                if (null == tempString) {

                    return "false";
                }

                return tempString;

            } catch (IOException e) {

                e.printStackTrace();
                return "false";

            } finally {

                if (reader != null) {

                    try {

                        reader.close();

                    } catch (IOException e1) {

                        e1.printStackTrace();

                    }
                }
            }
        }

        return "false";
    }

    /**
     * 将数字格式化
     * @param num 分钟和秒钟的数字
     * @return 固定格式的数字，如9改成09
     */
    public static String getMS(int num) {

        String newNum;

        if (num < 10) {

            newNum = "0" + num;

        } else {

            newNum = "" + num;

        }

        return newNum;
    }

    /**
     * 获取当前时间hour小时之前的时间字符串
     * @param hour 固定小时，指定为多少小时之前
     * @return yyyyMMddHH格式的字符串
     */
    public static String getYearToHour(int hour) {

        Date oldTime = new Date(System.currentTimeMillis() - hour * 60 * 60 * 1000);
        SimpleDateFormat sdFormatter = new SimpleDateFormat("yyyyMMddHH");
        return sdFormatter.format(oldTime);

    }

    /**
     * 根据key获取value
     * @param key 为kv数据表中的指定k，用来请求value
     * @param token 固定的请求数据时需要的参数
     * @return 请求到的数据
     * @throws Exception
     */
    public static String getValue(String key, String token) throws Exception {

        String getValueByKey = "kv/getValueByKey?token=" + token + "&table=kunyan_to_upload_inter_tab_mr&key=" + key;
        //System.out.println(getValueByKey);
        try {

            String value = doGet(getValueByKey);
            JSONObject jbKV = JSONObject.fromObject(value);
            String kv = jbKV.getString("result");

            if (!kv.equals("null")) {

                String valueBase64 = JSONObject.fromObject(kv).getString("value");
                return getFromBASE64(valueBase64);

            } else {

                return null;

            }

        } catch (JSONException e) {

            e.printStackTrace();

        }

        return "1";
    }

    /**
     * 获取电信的token的方法
     * @return 获取的token字符串
     * @throws Exception
     */
    public static String getToken() throws Exception {

        String apiKey = "98f5103019170612fd3a486e3d872c48";
        String userName = "e_kunyan";
        String password = "kunyan123";
        String getToken = "getToken?apiKey=" + apiKey + "&" + "sign=" + sign(md5Encode(password), userName + apiKey);
        JSONObject jbToken = JSONObject.fromObject(doGet(getToken));
        return jbToken.getString("result");

    }

    /**
     * 解码Base64字符串
     * @param str base64字符串
     * @return 解码后的字符串
     */
    public static String getFromBASE64(String str) {

        if (str == null) return null;

        BASE64Decoder decoder = new BASE64Decoder();

        try {

            byte[] bytes = decoder.decodeBuffer(str);
            return new String(bytes);

        } catch (Exception e) {

            e.printStackTrace();
            return null;

        }
    }


    /**
     * 此方法为http请求
     * @param toDo 指定所需的请求
     * @return 请求到的数据
     * @throws Exception
     */
    public static String doGet(String toDo) throws Exception {

        URL localURL = new URL("http://61.129.39.71/telecom-dmp/" + toDo);
        System.out.println(localURL);
        URLConnection connection = localURL.openConnection();
        HttpURLConnection httpURLConnection = (HttpURLConnection) connection;

        httpURLConnection.setConnectTimeout(30000);
        httpURLConnection.setReadTimeout(30000);
        httpURLConnection.setRequestProperty("Connection", "keep-alive");
        httpURLConnection.setRequestProperty("Accept-Charset", "utf-8");
        httpURLConnection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");

        InputStream inputStream = null;
        InputStreamReader inputStreamReader = null;
        BufferedReader reader = null;
        StringBuilder resultBuilder = new StringBuilder();
        String tempLine;

        try {

            if (httpURLConnection.getResponseCode() >= 300) {

                throw new Exception("HTTP Request is not success, Response code is " + httpURLConnection.getResponseCode());

            }

            inputStream = httpURLConnection.getInputStream();
            inputStreamReader = new InputStreamReader(inputStream);
            reader = new BufferedReader(inputStreamReader);

            while ((tempLine = reader.readLine()) != null) {

                resultBuilder.append(tempLine);

            }
        } catch (IOException e) {

            e.printStackTrace();

        } finally {

            if (reader != null) {

                reader.close();

            }

            if (inputStreamReader != null) {

                inputStreamReader.close();

            }

            if (inputStream != null) {

                inputStream.close();

            }
        }

        return resultBuilder.toString();
    }

    /**
     * 获取http请求时所需的签名
     * @param secretKey 经过md5加密处理的秘钥
     * @param data 用户名称和apiKey
     * @return 签名字符串
     * @throws Exception
     */
    public static String sign(String secretKey, String data) throws Exception {

        SecretKeySpec signingKey = new SecretKeySpec(secretKey.getBytes(), HMAC_SHA1_ALGORITHM);
        Mac mac = Mac.getInstance(HMAC_SHA1_ALGORITHM);
        mac.init(signingKey);
        byte[] rawHmac = mac.doFinal(data.getBytes());
        return Hex.encodeHexString(rawHmac);

    }

    /**
     * 对字符串做md5编码
     * @param str 需要md5编码的字符串
     * @return 做了md5编码之后的字符串
     * @throws Exception
     */
    public static String md5Encode(String str) throws Exception {

        MessageDigest md5;

        try {

            md5 = MessageDigest.getInstance("MD5");

        } catch (Exception e) {

            e.printStackTrace();
            return "";
        }

        byte[] byteArray = str.getBytes("UTF-8");
        byte[] md5Bytes = md5.digest(byteArray);
        StringBuilder hexValue = new StringBuilder();

        for (byte md5Byte : md5Bytes) {

            int val = ((int) md5Byte) & 0xff;
            if (val < 16) {

                hexValue.append("0");

            }

            hexValue.append(Integer.toHexString(val));
        }

        return hexValue.toString();
    }


    //类部类，线程类
    static class DoGetValue implements Runnable {

        private String s_min = "";
        private String s_sec = "";
        private String year_to_hour = "";
        private String key = "";
        private BufferedWriter writer = null;
        private int num;
        private String token;

        //构造方法，初始化类的变量
        public DoGetValue(String year_to_hour, String s_min, int num, String token) {

            this.num = num;
            this.s_min = s_min;
            this.year_to_hour = year_to_hour;
            this.token = token;

        }

        @Override
        public void run() {
//            String filesPath = "/home/liaochengming/shdx/kv_down_files/";
            String filesPath = "F:\\shdx\\";
            File writer_file;
            String fileName = year_to_hour + num + ".txt";
            writer_file = new File(filesPath + fileName);

            try {

                writer = new BufferedWriter(new FileWriter(writer_file));

                for (int i = 0; i < 60; i++) {

                    if (i < 10) {

                        s_sec = "0" + i;

                    } else {

                        s_sec = "" + i;

                    }

                    for (int k = 1; k < 2500; k++) {

                        key = this.year_to_hour + this.s_min + this.s_sec + k;
                        String value = SHKVDown.getValue(key, token);

                        if (null == value) {

                            break;

                        } else if (value.equals("1")) {

                            Logger.getLogger("kv_down").info("kv down exception!");

                        } else {

                            writer.write(value);
                            writer.write("\r\n");
                            writer.flush();

                        }
                    }
                }

                writer.close();

            } catch (Exception e) {

                e.printStackTrace();

            }

        }
    }
}
