package com.aug3.test.io.avro;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

import org.apache.avro.file.DataFileReader;
import org.apache.avro.file.DataFileWriter;
import org.apache.avro.io.DatumReader;
import org.apache.avro.io.DatumWriter;
import org.apache.avro.specific.SpecificDatumReader;
import org.apache.avro.specific.SpecificDatumWriter;

public class AvroTest {

	public static void main(String[] args) {

		List<UriSpec> uris = new ArrayList<>();
		uris.add(UriSpec.newBuilder().setHost("192.168.0.86").setPort(1080).setScheme(ProtocolType.HTTP).build());
		uris.add(UriSpec.newBuilder().setHost("192.168.0.88").setPort(2080).setScheme(ProtocolType.HTTP).build());
		uris.add(UriSpec.newBuilder().setHost("192.168.0.89").setPort(3080).setScheme(ProtocolType.HTTP).build());
		uris.add(UriSpec.newBuilder().setHost("192.168.0.90").setPort(1080).setScheme(ProtocolType.HTTP).build());

		ServiceInstance si = ServiceInstance.newBuilder().setName("hqservice").setId(1).setUri(uris)
				.setTs(Instant.now().toEpochMilli()).build();

		long t1 = System.currentTimeMillis();
		File f = new File("servicepool.avro");
		try {

			DatumWriter<ServiceInstance> userDatumWriter = new SpecificDatumWriter<ServiceInstance>(
					ServiceInstance.class);
			DataFileWriter<ServiceInstance> dataFileWriter = new DataFileWriter<ServiceInstance>(userDatumWriter);
			dataFileWriter.create(si.getSchema(), f);
			dataFileWriter.append(si);
			dataFileWriter.close();

			DatumReader<ServiceInstance> userDatumReader = new SpecificDatumReader<ServiceInstance>(
					ServiceInstance.class);
			DataFileReader<ServiceInstance> dataFileReader = new DataFileReader<ServiceInstance>(f, userDatumReader);
			ServiceInstance si2 = null;
			while (dataFileReader.hasNext()) {
				// Reuse user object by passing it to next(). This saves us from
				// allocating and garbage collecting many objects for files with
				// many items.
				si2 = dataFileReader.next(si2);
			}
			dataFileReader.close();
			System.out.println(si2.getName());

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		System.out.println(System.currentTimeMillis() - t1);

	}

}
