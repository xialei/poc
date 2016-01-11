package com.aug3.test.hbase;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;

public class HBaseConfigUtils {

	public static Configuration getHBaseConfig() {

		Configuration conf = HBaseConfiguration.create();
		conf.set("hbase.master","192.168.250.208");
//		conf.set("fs.defaultFS", "hdfs://192.168.250.208:9000/");
//		conf.set("mapreduce.framework.name", "yarn");
//		conf.set("yarn.resourcemanager.address", "192.168.250.208:8032");
//		conf.set("mapred.job.tracker", "192.168.250.208:9001");
		conf.set("hbase.zookeeper.quorum", "192.168.250.208:2181");

		return conf;

	}

}
