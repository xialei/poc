package com.aug3.test.my;

import java.util.HashSet;
import java.util.Set;

public class StringTest {

	public static void main(String args[]) {

		String url = "http://www.bloomfilter.com/";
		Set s = new HashSet<String>();
		for (int i = 0; i < 200000; i++) {

			long t1 = System.currentTimeMillis();

			String newurl = url + i;

			s.add(newurl);
			System.out.println(s.contains(newurl));

			long t2 = System.currentTimeMillis();

			System.out.println(t2 - t1);
		}

		System.out.println(String.valueOf(null));
	}

}
