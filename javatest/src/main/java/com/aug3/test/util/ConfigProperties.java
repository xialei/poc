package com.aug3.test.util;

import java.util.Properties;
import java.util.Vector;

import org.apache.log4j.Logger;

/**
 * Global configuration file loader. All key-value pairs are loaded into the jvm
 * static variable config.
 * 
 * @author Roger.xia
 * 
 */
public class ConfigProperties {

	private static final Logger log = Logger.getLogger(ConfigProperties.class);

	private static Properties config = new Properties();

	private static Vector<String> kv = new Vector<String>();

	public ConfigProperties(String propertyFile) {

		if (!kv.contains(propertyFile)) {
			kv.add(propertyFile);
			config.putAll(new PropertyLoader(propertyFile));

			log.debug("imported " + config.size() + " configuration records.");
		}
	}

	public ConfigProperties(String[] propertyFiles) {
		for (String file : propertyFiles) {
			if (!kv.contains(file)) {
				kv.add(file);
				config.putAll(new PropertyLoader(file));

			}
		}
		log.debug("imported " + config.size() + " configuration records.");
	}

	public void clear() {
		kv.clear();
		config.clear();
	}

	public String getProperty(String key, String defaultValue) {
		return config.getProperty(key, defaultValue);
	}

	public String getProperty(String key) {
		return config.getProperty(key);
	}

	public int getIntProperty(String key, int defaultValue) {
		String value = getProperty(key);
		try {
			return value == null ? defaultValue : Integer.parseInt(getProperty(key));
		} catch (NumberFormatException e) {
			log.info("Wrong int value for property key " + key + " , default value used.");
			return defaultValue;
		}
	}

	public int getIntProperty(String key) {
		return Integer.parseInt(getProperty(key));
	}

	public boolean getBooleanProperty(String key) {
		return Boolean.valueOf(getProperty(key));
	}

	public boolean getBooleanProperty(String key, boolean defaultValue) {
		String value = getProperty(key);
		return value == null ? defaultValue : Boolean.valueOf(getProperty(key));
	}
	
	public Properties getProperties() {
	    return config;
	}

	public String toString() {

		StringBuilder s = new StringBuilder();

		for (String file : kv) {
			s.append(file).append(":");
		}
		s.append(config.toString());

		return s.toString();
	}

}
