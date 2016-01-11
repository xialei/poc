namespace java com.aug3.test.io.thrift

enum ProtocolType {
	HTTP,
	RPC,
	AMQP
}

struct UriSpec {
	1: required string host,
	2: required i32 port,
	3: optional ProtocolType type
}

struct ServiceInstance {
	1: required string name,
	2: required i32 id,
	3: required list<UriSpec> uri,
	4: optional i64 ts
}

service ServicePool {
	bool registerService(1: ServiceInstance si)
}