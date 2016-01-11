package com.aug3.example;

import java.util.Date;

public class Management {

	private String code;

	private String name;

	private boolean sex;

	private Date from;

	private Date end = null;

	private String experience;

	private boolean dismiss = false;

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

	public boolean isSex() {
		return sex;
	}

	public void setSex(boolean sex) {
		this.sex = sex;
	}

	public Date getFrom() {
		return from;
	}

	public void setFrom(Date from) {
		this.from = from;
	}

	public Date getEnd() {
		return end;
	}

	public void setEnd(Date end) {
		this.end = end;
	}

	public String getExperience() {
		return experience;
	}

	public void setExperience(String experience) {
		this.experience = experience;
	}

	public boolean isDismiss() {
		return dismiss;
	}

	public void setDismiss(boolean dismiss) {
		this.dismiss = dismiss;
	}

}
