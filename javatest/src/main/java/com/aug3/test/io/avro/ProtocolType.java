/**
 * Autogenerated by Avro
 * 
 * DO NOT EDIT DIRECTLY
 */
package com.aug3.test.io.avro;  
@SuppressWarnings("all")
@org.apache.avro.specific.AvroGenerated
public enum ProtocolType { 
  HTTP, RPC, AMQP  ;
  public static final org.apache.avro.Schema SCHEMA$ = new org.apache.avro.Schema.Parser().parse("{\"type\":\"enum\",\"name\":\"ProtocolType\",\"namespace\":\"com.aug3.test.io.avro\",\"symbols\":[\"HTTP\",\"RPC\",\"AMQP\"]}");
  public static org.apache.avro.Schema getClassSchema() { return SCHEMA$; }
}