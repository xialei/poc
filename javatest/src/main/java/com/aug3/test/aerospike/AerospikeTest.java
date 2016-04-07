package com.aug3.test.aerospike;

import com.aerospike.client.AerospikeClient;
import com.aerospike.client.Bin;
import com.aerospike.client.Key;
import com.aerospike.client.Record;
import com.aerospike.client.policy.ClientPolicy;

public class AerospikeTest {

	// private static void asyncPutGet(){
	//
	// }
	
	public static void main(String[] args) {

		ClientPolicy policy = new ClientPolicy();
		policy.readPolicyDefault.timeout = 50;    
		policy.readPolicyDefault.maxRetries = 1;
		policy.readPolicyDefault.sleepBetweenRetries = 10;
		policy.writePolicyDefault.timeout = 200;    
		policy.writePolicyDefault.maxRetries = 1;
		policy.writePolicyDefault.sleepBetweenRetries = 50;
		
		AerospikeClient client = new AerospikeClient(policy, "192.168.0.229", 3000);

		Key key = new Key("test", "demo", "putgetkey");
		Bin b1 = new Bin("b1", "v1");
		Bin b2 = new Bin("b2", "v2");

		client.put(null, key, b1, b2);

		Record record = client.get(null, key);
		
		client.delete(null, key);
		
		

		client.close();
	}

}
