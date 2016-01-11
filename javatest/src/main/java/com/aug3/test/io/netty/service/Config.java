package com.aug3.test.io.netty.service;

public class Config {
	public static String getRealPath(String uri) {
		StringBuilder sb = new StringBuilder("D://");
		sb.append(uri);
		if (!uri.endsWith("/")) {
			sb.append('/');
		}
		return sb.toString();
	}
}
