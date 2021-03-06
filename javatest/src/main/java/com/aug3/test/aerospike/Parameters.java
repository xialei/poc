package com.aug3.test.aerospike;

import java.util.Map;

import com.aerospike.client.AerospikeClient;
import com.aerospike.client.Info;
import com.aerospike.client.cluster.Node;
import com.aerospike.client.policy.Policy;
import com.aerospike.client.policy.WritePolicy;

/**
 * https://github.com/aerospike/aerospike-client-java
 * 
 * @author roger.xia
 *
 */
public class Parameters {

	String host;
	int port;
	String user;
	String password;
	String namespace;
	String set;
	WritePolicy writePolicy;
	Policy policy;
	boolean singleBin;
	boolean hasGeo;
	boolean hasUdf;
	boolean hasLargeDataTypes;
	boolean hasCDTList;

	protected Parameters(String host, int port, String user, String password, String namespace,
			String set) {
		this.host = host;
		this.port = port;
		this.user = user;
		this.password = password;
		this.namespace = namespace;
		this.set = set;
	}

	/**
	 * Some database calls need to know how the server is configured.
	 */
	protected void setServerSpecific(AerospikeClient client) throws Exception {
		Node node = client.getNodes()[0];
		String featuresFilter = "features";
		String namespaceFilter = "namespace/" + namespace;
		Map<String, String> tokens = Info.request(null, node, featuresFilter, namespaceFilter);

		String features = tokens.get(featuresFilter);
		hasGeo = false;
		hasUdf = false;
		hasCDTList = false;

		if (features != null) {
			String[] list = features.split(";");

			for (String s : list) {
				if (s.equals("geo")) {
					hasGeo = true;
				} else if (s.equals("udf")) {
					hasUdf = true;
				} else if (s.equals("cdt-list")) {
					hasCDTList = true;
				}
			}
		}

		String namespaceTokens = tokens.get(namespaceFilter);

		if (namespaceTokens == null) {
			throw new Exception(String.format(
					"Failed to get namespace info: host=%s port=%d namespace=%s", host, port,
					namespace));
		}

		singleBin = parseBoolean(namespaceTokens, "single-bin");
		hasLargeDataTypes = parseBoolean(namespaceTokens, "ldt-enabled");
	}

	private static boolean parseBoolean(String namespaceTokens, String name) {
		String search = name + '=';
		int begin = namespaceTokens.indexOf(search);

		if (begin < 0) {
			return false;
		}

		begin += search.length();
		int end = namespaceTokens.indexOf(';', begin);

		if (end < 0) {
			end = namespaceTokens.length();
		}

		String value = namespaceTokens.substring(begin, end);
		return Boolean.parseBoolean(value);
	}

	@Override
	public String toString() {
		return "Parameters: host=" + host + " port=" + port + " ns=" + namespace + " set=" + set
				+ " single-bin=" + singleBin;
	}

	public String getBinName(String name) {
		// Single bin servers don't need a bin name.
		return singleBin ? "" : name;
	}

}
