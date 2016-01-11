package com.aug3.test.io.netty;

public class NettyClient {

	final static String host = "127.0.0.1";
	final static int port = 8080;

	public static void main(String[] args) {
		Client client = new Client();
		client.config(host, port).start();
	}
}
