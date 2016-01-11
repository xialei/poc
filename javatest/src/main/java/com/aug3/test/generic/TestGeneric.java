package com.aug3.test.generic;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

public class TestGeneric {

	private static void test(Map<String, ? extends Serializable> m) {

		System.out.println(((Obj) m.get("roger")).getName());

	}

	private static <T> Map<String, T> test2(Map<String, Object> m, Class<T> claz) {

		Map<String, T> map = new HashMap<String, T>();

		for (String key : m.keySet()) {
			map.put(key, (T) m.get(key));
		}

		return map;

	}

	public static void main(String[] args) {
		Map<String, Obj> m = new HashMap<String, Obj>();
		Obj o = new Obj();
		o.setName("Roger");
		o.setAge(31);
		m.put("roger", o);
		m.put("tim", o);

		test(m);

		Map<String, Object> m2 = new HashMap<String, Object>();
		Obj o2 = new Obj();
		o2.setName("Roger");
		o2.setAge(31);
		m2.put("roger", o2);
		m2.put("tim", o2);

		Map<String, Obj> ret = test2(m2, Obj.class);
		System.out.println(ret.get("roger").getName());

	}

}
