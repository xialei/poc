package com.aug3.test.json;

import java.lang.reflect.Type;
import java.util.Map;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import com.google.gson.reflect.TypeToken;

public class JSONMap {

	public static void main(String[] args) {

		String jsonString = "{k:orgname,p1:pv1,p2:pv2,p3:pv3}";

		long t1 = System.currentTimeMillis();
		JsonElement root = new JsonParser().parse(jsonString);
		String k = root.getAsJsonObject().get("k").getAsString();
		long t2 = System.currentTimeMillis();
		System.out.println(k);
		System.out.println(t2 - t1);

		Type mapType = new TypeToken<Map<String, String>>() {
		}.getType();
		Map<String, String> gson = new Gson().fromJson(jsonString, mapType);
		long t3 = System.currentTimeMillis();
		System.out.println(gson.get("k"));
		System.out.println(t3 - t2);

		jsonString = "{k:{orgname:pkey, reg:pkey1},pkey:{p1:pv1,p2:pv2,p3:pv3}, pkey1:{p1:pv1,p2:pv2}}";

		mapType = new TypeToken<Map<String, Map<String, String>>>() {
		}.getType();
		Map<String, Map<String, String>> gsonM = new Gson().fromJson(jsonString, mapType);
		System.out.println(gsonM.get("k").keySet());
		System.out.println(gsonM.get(gsonM.get("k").get("orgname")));

	}

}
