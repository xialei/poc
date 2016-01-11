package com.aug3.test.io.thrift;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

public class ThriftTest {

	public static void main(String[] args) {

		ServiceInstance si = new ServiceInstance();
		si.setName("hqservice");
		si.setId(1);
		si.setTs(Instant.now().toEpochMilli());

		UriSpec uri = new UriSpec();
		uri.setHost("192.168.0.86");
		uri.setPort(8080);
		uri.setType(ProtocolType.HTTP);

		List<UriSpec> urilist = new ArrayList<>();
		urilist.add(uri);

		si.setUri(urilist);
		

	}
}
