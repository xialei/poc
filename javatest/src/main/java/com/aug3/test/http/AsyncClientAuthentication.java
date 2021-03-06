package com.aug3.test.http;

import java.util.concurrent.Future;

import org.apache.http.HttpResponse;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.nio.client.CloseableHttpAsyncClient;
import org.apache.http.impl.nio.client.HttpAsyncClients;

/**
 * A simple example that uses HttpClient to execute an HTTP request against a
 * target site that requires user authentication.
 */
public class AsyncClientAuthentication {

	public static void main(String[] args) throws Exception {
		CredentialsProvider credsProvider = new BasicCredentialsProvider();
		credsProvider.setCredentials(new AuthScope("login.sina.com.cn", AuthScope.ANY_PORT, AuthScope.ANY_REALM),
				new UsernamePasswordCredentials("roger_xl", "xyz"));
		CloseableHttpAsyncClient httpclient = HttpAsyncClients.custom().setDefaultCredentialsProvider(credsProvider)
				.build();
		try {
			HttpGet httpget = new HttpGet("http://login.sina.com.cn/");

			System.out.println("Executing request " + httpget.getRequestLine());
			Future<HttpResponse> future = httpclient.execute(httpget, null);
			HttpResponse response = future.get();
			System.out.println("Response: " + response.getStatusLine());
			System.out.println("Shutting down");
		} finally {
			httpclient.close();
		}
	}
}