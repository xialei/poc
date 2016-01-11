package com.aug3.test.mongodb;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

import org.bson.BSONObject;
import org.bson.BasicBSONDecoder;
import org.bson.types.BasicBSONList;

import com.aug3.test.util.ConfigProperties;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

public class TestMongo {

	public static void main(String[] args) throws FileNotFoundException, IOException {
		ConfigProperties cfg = new ConfigProperties("/javatest.properties");

		String bson = cfg.getProperty("bson");
		String json = cfg.getProperty("json");

		// FileInputStream fis = new FileInputStream(new
		// File("D:\\fin_rpt_asrep_ext_ytd_635319465381787242_1.data"));
		FileInputStream fis = new FileInputStream(new File("D:\\ced_indicator_data_635349839910088265_0.mongo"));

		byte[] b1 = new byte[fis.available()];
		fis.read(b1);

		BSONObject dbObj;
		dbObj = (BSONObject) new BasicBSONDecoder().readObject(b1);
		System.out.println(dbObj.toString());
		BasicBSONList dblist = (BasicBSONList) dbObj.get("datas");
		BSONObject dbo = (BSONObject) dblist.get(0);
		DBObject myObj = new BasicDBObject();
		myObj.putAll((BSONObject) dbo.get("o"));
		Object id = myObj.get("code");

		if (id instanceof Integer)
			System.out.println("int");
		else if (id instanceof Long)
			System.out.println("long");
		else
			System.out.println("non");

		fis.close();

		// char[] ca = "\n".toCharArray();
		// for (char c : ca) {
		// System.out.println(Integer.toBinaryString(c));
		// }

		// System.out.println(bson);

		// DBObject dbObj = (DBObject) JSON.parse(json);
		// BSONObject dbObj = JSONUtil.fromJson(bson, BSONObject.class);
		// BSONObject dbObj = (BSONObject) new
		// BasicBSONDecoder().readObject(bson.getBytes());

		// BSONObject dbObj =
		// DefaultDBDecoder.FACTORY.create().decode(bson.getBytes(),
		// (DBCollection) null);

		// System.out.println(dbObj.get("upt"));
	}

}
