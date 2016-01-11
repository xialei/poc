package com.aug3.test.io.pb;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.time.Instant;

import com.aug3.test.io.pb.ServicePoolProtos.ServiceInstance;
import com.aug3.test.io.pb.ServicePoolProtos.ServiceInstance.UriSpec;
import com.google.protobuf.InvalidProtocolBufferException;

public class ProtobufTest {

	public static void main(String[] args) {

		ServiceInstance si = ServiceInstance
				.newBuilder()
				.setName("hqservice")
				.setId(1)
				.setTs(Instant.now().toEpochMilli())
				.addUri(UriSpec.newBuilder().setHost("192.168.0.86").setPort(8080)
						.setType(ServiceInstance.ProtocolType.HTTP))
				.addUri(UriSpec.newBuilder().setHost("192.168.0.88").setPort(1008)
						.setType(ServiceInstance.ProtocolType.HTTP))
				.addUri(UriSpec.newBuilder().setHost("192.168.0.90").setPort(1009)
						.setType(ServiceInstance.ProtocolType.HTTP))
				.addUri(UriSpec.newBuilder().setHost("192.168.0.92").setPort(1010)
						.setType(ServiceInstance.ProtocolType.HTTP))
				.addUri(UriSpec.newBuilder().setHost("192.168.0.95").setPort(1012)
						.setType(ServiceInstance.ProtocolType.HTTP)).build();

		System.out.println(si.getSerializedSize());

		long t1 = System.currentTimeMillis();
		String f = "D://fos.txt";
		try {

			FileOutputStream fos = new FileOutputStream(f);
			si.writeTo(fos);

			FileInputStream fis = new FileInputStream(f);
			ServiceInstance si2 = ServiceInstance.parseFrom(fis);
			System.out.println(si2.getName());

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		System.out.println(System.currentTimeMillis() - t1);
		System.out.println(si.toString());
		
		long t2 = System.currentTimeMillis();

		for (int i = 0; i < 10000; i++) {
			byte[] b = si.toByteArray();
			ServiceInstance si3;
			try {
				si3 = ServiceInstance.parseFrom(b);
				// System.out.println(si3.getName());
			} catch (InvalidProtocolBufferException e) {
				e.printStackTrace();
			}
		}

		System.out.println(System.currentTimeMillis() - t2);

	}
}
