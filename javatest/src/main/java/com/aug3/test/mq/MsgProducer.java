package com.aug3.test.mq;

import java.util.Date;
import java.util.Properties;
import java.util.Random;

import kafka.javaapi.producer.Producer;
import kafka.producer.KeyedMessage;
import kafka.producer.ProducerConfig;

public class MsgProducer {

	public static void main(String[] args) {
		Properties props = new Properties();
		props.put("metadata.broker.list", "192.168.0.233:9092");
		//props.put("zookeeper.connect", "192.168.0.229:2181/kafka");
		props.put("serializer.class", "kafka.serializer.StringEncoder");
		props.put("partitioner.class", "com.aug3.test.mq.SimplePartitioner");
		props.put("request.required.acks", "1");
		ProducerConfig config = new ProducerConfig(props);
		Producer<String, String> producer = new Producer<String, String>(config);

		int events = 10;
		Random rnd = new Random();
		for (long nEvents = 0; nEvents < events; nEvents++) {
			long runtime = new Date().getTime();
			String ip = "192.168.2." + rnd.nextInt(255);
			String msg = runtime + ",www.example.com," + ip;
			KeyedMessage<String, String> data = new KeyedMessage<String, String>("test", ip, msg);
			producer.send(data);
		}

		producer.close();

	}
}
