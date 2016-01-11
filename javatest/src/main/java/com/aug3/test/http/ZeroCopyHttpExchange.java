package com.aug3.test.http;

import java.io.File;
import java.util.concurrent.Future;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.entity.ContentType;
import org.apache.http.impl.nio.client.CloseableHttpAsyncClient;
import org.apache.http.impl.nio.client.HttpAsyncClients;
import org.apache.http.nio.client.methods.ZeroCopyConsumer;
import org.apache.http.nio.client.methods.ZeroCopyPost;

/**
 * This example demonstrates how HttpAsyncClient can be used to upload or
 * download files without creating an intermediate content buffer in memory
 * (zero copy file transfer).
 */
public class ZeroCopyHttpExchange {

	public static void main(final String[] args) throws Exception {
		CloseableHttpAsyncClient httpclient = HttpAsyncClients.createDefault();
		try {
			httpclient.start();
			File upload = new File("D:\\shengbang.txt");
			File download = new File("x.txt");
			ZeroCopyPost httpost = new ZeroCopyPost("http://192.168.0.227:18080/", upload, ContentType.create("text/plain"));
			ZeroCopyConsumer<File> consumer = new ZeroCopyConsumer<File>(download) {

				@Override
				protected File process(final HttpResponse response, final File file, final ContentType contentType)
						throws Exception {
					if (response.getStatusLine().getStatusCode() != HttpStatus.SC_OK) {
						throw new ClientProtocolException("Upload failed: " + response.getStatusLine());
					}
					return file;
				}

			};
			Future<File> future = httpclient.execute(httpost, consumer, null);
			File result = future.get();
			System.out.println("Response file length: " + result.length());
			System.out.println("Shutting down");
		} finally {
			httpclient.close();
		}
		System.out.println("Done");
	}

}