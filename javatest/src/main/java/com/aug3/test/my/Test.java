package com.aug3.test.my;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class Test {

	private static final DecimalFormat df = new DecimalFormat("000000");

	public static void main(String args[]) {

		String ss = "s,";
		System.out.print(ss.split(",").length);

		System.out.println(1405160000001l);
		System.out.println(df.format(100));
		System.out.println("/app/datapub/xyz.zip.md5".substring(0, "/app/datapub/xyz.zip.md5".length() - 4));
		System.out.println(f.CFP.ordinal());
		System.out.println(5000 << 10000);

		try {
			System.out.println(Inet4Address.getLocalHost().getHostAddress());
		} catch (UnknownHostException e1) {
		}

		Enumeration en;
		try {
			en = NetworkInterface.getNetworkInterfaces();
			while (en.hasMoreElements()) {
				NetworkInterface ni = (NetworkInterface) en.nextElement();
				Enumeration ee = ni.getInetAddresses();
				while (ee.hasMoreElements()) {
					InetAddress ia = (InetAddress) ee.nextElement();
					System.out.println(ia.getHostAddress());
				}
			}
		} catch (SocketException e1) {
			e1.printStackTrace();
		}

		List<String> list1 = new ArrayList<String>();
		list1.add("1");
		list1.add("2");
		list1.add("3");
		list1.add("4");
		list1.add("5");
		list1.add("6");

		int numSecu = list1.size();
		int step = 3;
		int mod = numSecu % step;
		int loop = numSecu / step + (mod > 0 ? 1 : 0);
		System.out.println(loop);
		for (int i = 0; i < loop; i++) {
			System.out.println(list1.subList(i * step, (i + 1) * step > numSecu ? numSecu : (i + 1) * step));
		}

		List<String> list2 = new ArrayList<String>();
		list2.add("a");
		list2.add("b");
		System.out.println(list1.subList(1, 2));
		Collections.sort(list2);
		System.out.println(list1.toString());
		System.out.println(list2.toString());

		Calendar cal = Calendar.getInstance();
		cal.add(Calendar.DAY_OF_YEAR, -1);
		System.out.println(cal.getTime());
		Calendar cal2 = Calendar.getInstance();
		cal2.add(Calendar.DAY_OF_YEAR, -1);
		System.out.println(cal2.getTime());

		BigDecimal five = new BigDecimal("5");
		BigDecimal fourPointTwo = new BigDecimal("4.2");
		// System.out.println(five.divide(fourPointTwo));
		System.out.println(five.divide(fourPointTwo, 2, RoundingMode.HALF_UP));
		System.out.println(five.divide(fourPointTwo, 16, RoundingMode.HALF_UP));

		final List<String> list = new ArrayList<String>();
		list.add("a");
		list.add("b");
		System.out.println(list.hashCode());

		final List<String> listcopy = new ArrayList<String>();
		listcopy.add("b");
		listcopy.add("a");
		System.out.println(listcopy.hashCode());

		Set s = new HashSet<String>();
		s.add("a");
		s.add("bba");

		Set s2 = new HashSet<String>();
		s2.add("bba");
		s2.add("a");

		System.out.println(s.hashCode());
		System.out.println(s2.hashCode());

		s2.remove("a");
		s2.removeAll(s);
		System.out.println(s2.size());

		System.out.println(1 % 20);

		InetAddress addr;
		try {
			addr = InetAddress.getLocalHost();
			System.out.println(addr.getHostAddress());
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		Map<String, Double> mm = new ConcurrentHashMap<String, Double>();
		mm.put("secu", null);

	}

	public enum f {
		CFP, CFH;
	}

}
