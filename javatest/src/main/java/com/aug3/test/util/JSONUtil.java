package com.aug3.test.util;

import java.lang.reflect.Type;
import java.util.Collection;
import java.util.Enumeration;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.apache.commons.lang.StringUtils;
import org.apache.log4j.Logger;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.reflect.TypeToken;

/**
 * @author Roger.xia
 * 
 *         We use this class to convert Object to JSON string and reverse.
 * 
 *         This implementation is currently based on GSON.
 * 
 */
public class JSONUtil {

	private static final Logger logger = Logger.getLogger("JSONUtil.class");

	public static final String EMPTY_JSON = "{}";
	public static final String EMPTY_JSON_ARRAY = "[]";

	private JSONUtil() {

	}

	private static final GsonBuilder builder = new GsonBuilder();

	private static final Gson gson = builder.serializeNulls().create();

	/**
	 * 
	 * by default,this method allows serialize null-value properties
	 * 
	 * @param src
	 * @return
	 */
	public static String toJson(Object src) {
		if (src == null) {
			return EMPTY_JSON;
		}
		return gson.toJson(src);
	}

	/**
	 * default is medium : Mar 8, 2013 12:00:00 AM
	 * 
	 * @param obj
	 * @param dateFormat
	 *            Note that this pattern must abide by the convention provided
	 *            by SimpleDateFormat class.
	 * @return
	 */
	public static String toJson(Object obj, String dateFormat) {
		if (obj == null) {
			return EMPTY_JSON;
		} else if (StringUtils.isBlank(dateFormat)) {
			return gson.toJson(obj);
		}

		try {
			return builder.setDateFormat(dateFormat).create().toJson(obj);
		} catch (Exception e) {

			logger.error("Exception for toJson(obj, dateFormat) : " + e.getMessage());
			return gson.toJson(obj);
		}
	}

	public static String toJson(Object target, Type targetType) {

		String result = EMPTY_JSON;

		if (target == null)
			return result;

		try {
			if (targetType != null) {
				result = gson.toJson(target, targetType);
			} else {
				result = gson.toJson(target);
			}
		} catch (Exception ex) {
			logger.error("JSONUtil.toJson(target, targetType) exception, return empty json, exception for "
					+ target.toString() + " : " + ex.getMessage());
			if (target instanceof Collection || target instanceof Iterator || target instanceof Enumeration
					|| target.getClass().isArray()) {
				result = EMPTY_JSON_ARRAY;
			} else
				result = EMPTY_JSON;
		}
		return result;
	}

	/**
	 * 
	 * to covert a string to a class
	 * 
	 * @param json
	 * @param classOfT
	 * @return
	 */
	public static <T> T fromJson(String json, Class<T> classOfT) {
		return gson.fromJson(json, classOfT);
	}

	public static <T> T fromJson(String json, Type type) {
		return gson.fromJson(json, type);
	}

	/**
	 * 
	 * to covert a JsonElement to a class
	 * 
	 * @param json
	 * @param classOfT
	 * @return
	 */
	public static <T> T fromJson(JsonElement jsonElem, Class<T> classOfT) {
		return gson.fromJson(jsonElem, classOfT);
	}

	/**
	 * convert json string to list
	 * 
	 * @param jsonStr
	 * @param type
	 * @return
	 */
	public static List<?> jsonToList(String json, Type type) {
		List<?> objList = gson.fromJson(json, type);
		return objList;
	}

	/**
	 * convert json to map
	 * 
	 * @param jsonStr
	 * @return
	 */
	public static Map<?, ?> jsonToMap(String json) {
		Type type = new TypeToken<Map<?, ?>>() {
		}.getType();
		Map<?, ?> objMap = gson.fromJson(json, type);
		return objMap;
	}

	public static void main(String[] args) {

	}

}
