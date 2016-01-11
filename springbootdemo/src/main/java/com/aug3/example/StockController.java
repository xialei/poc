package com.aug3.example;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class StockController {

	@RequestMapping("/stock")
	public BaseStock getStock() {

		BaseStock bs = new BaseStock();
		bs.setCode("601398_SH_EQ");
		bs.setName("工商银行");
		bs.setAddr("shanghai");
		bs.setOrgid("100000001");

		Management mgr = new Management();
		mgr.setCode("10001");
		try {
			mgr.setFrom(new SimpleDateFormat("YYYY-MM-DD").parse("2014-01-01"));
		} catch (ParseException e) {
		}
		mgr.setName("Alexander");
		mgr.setSex(true);
		mgr.setExperience("2000年毕业于哈佛大学");

		List<Management> mgrs = new ArrayList<>();
		mgrs.add(mgr);

		bs.setManagers(mgrs);

		String[] tags = new String[] { "bank", "fortune 50" };
		bs.setTags(tags);

		return bs;
	}

	@RequestMapping(value = "/stock/new", method = RequestMethod.POST)
	public String newStock(@RequestBody BaseStock stock) {

		return stock.getName();
	}

	// public static void main(String[] args) {
	// SpringApplication.run(StockController.class, args);
	// }
}
