spingboot demo
==============

spring initializr
-----------------

> http://start.spring.io/

> http://docs.spring.io/spring-boot/docs/current-SNAPSHOT/reference/htmlsingle/#boot-documentation

configure
---------

> application.properties
	
	spring mvc date format
	jackson date format
	
	tomcat threads
	
	server port \ ip \ context path
	
Test
----


deploy
------

> embbed web server

	mvn clean install
	java -Xmx1024m -Xss256k -jar target/springbootdemo-0.0.1-SNAPSHOT.jar
	
> standalone tomcat server

	Spring Boot也支持将应用部署至已有的Tomcat容器, 或JBoss, WebLogic等传统Java EE应用服务器。
	以Maven为例，首先需要将<packaging>从jar改成war，然后取消spring-boot-maven-plugin，然后修改Application.java：
	
	@Configuration
	@ComponentScan
	@EnableAutoConfiguration
	public class Application extends SpringBootServletInitializer {

	    public static void main(String[] args) {
	        SpringApplication.run(applicationClass, args);
	    }
	
	    @Override
	    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
	        return application.sources(applicationClass);
	    }
	
	    private static Class<Application> applicationClass = Application.class;
	}
	
thirdparty
----------

> redis
> mongodb
> properties file


profile
-------

	@Profile("dev")
	@Profile("prod")
	