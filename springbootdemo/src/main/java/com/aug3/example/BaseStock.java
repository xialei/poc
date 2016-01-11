package com.aug3.example;

import java.util.List;

public class BaseStock {

	private String code;

	private String name;

	private String orgid;

	private String addr;

	private List<Management> managers;

	private String[] tags;

	public String getCode() {
		return code;
	}

	public void setCode(String code) {
		this.code = code;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getOrgid() {
		return orgid;
	}

	public void setOrgid(String orgid) {
		this.orgid = orgid;
	}

	public String getAddr() {
		return addr;
	}

	public void setAddr(String addr) {
		this.addr = addr;
	}

	public List<Management> getManagers() {
		return managers;
	}

	public void setManagers(List<Management> managers) {
		this.managers = managers;
	}

	public String[] getTags() {
		return tags;
	}

	public void setTags(String[] tags) {
		this.tags = tags;
	}

}
