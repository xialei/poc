package com.aug3.test.hbase;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.MasterNotRunningException;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.HBaseAdmin;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.filter.FilterList;
import org.apache.hadoop.hbase.filter.PageFilter;
import org.apache.hadoop.hbase.filter.PrefixFilter;
import org.apache.hadoop.hbase.util.Bytes;

import com.google.protobuf.ServiceException;

public class EquityPriceExample {

	private final static String tableName = "equity_price";
	private final static String familyName = "hq";

	// private static void
	public static void main(String[] args) throws Exception {
		hbase();
	}

	private static void hbase() throws Exception {

		Configuration conf = HBaseConfigUtils.getHBaseConfig();

		try {
			HBaseAdmin.checkHBaseAvailable(conf);
		} catch (MasterNotRunningException e) {
			System.out.println("HBase is not running.");
			return;
		} catch (ServiceException e) {
			e.printStackTrace();
			return;
		}

		System.out.println("start");

		// 插入表数据
		HTable table = new HTable(conf, tableName);

		long t1 = System.currentTimeMillis();

		String rowkey = "000001_SZ_EQ:9223370614912375807";
		Get get = new Get(rowkey.getBytes());

		Result r = table.get(get);

		if (r != null) {
			printRecoder(r);
		}

		long t2 = System.currentTimeMillis();
		System.out.println(t2 - t1);

		Scan scan = new Scan();
		FilterList filterList = new FilterList();
		filterList.addFilter(new PrefixFilter(Bytes.toBytes("600000_")));
		filterList.addFilter(new PageFilter(1));
		scan.setFilter(filterList);

		ResultScanner rs = table.getScanner(scan);

		if (rs != null) {
			printRecoder(rs.next());
		}

		long t3 = System.currentTimeMillis();
		System.out.println(t3 - t2);

		table.close();
	}

	private static void printRecoder(Result result) throws Exception {
		for (Cell cell : result.rawCells()) {
			System.out.print("行健: " + new String(CellUtil.cloneRow(cell)));
			System.out.print("列簇: " + new String(CellUtil.cloneFamily(cell)));
			System.out.print(" 列: " + new String(CellUtil.cloneQualifier(cell)));
			System.out.print(" 值: " + new String(CellUtil.cloneValue(cell)));
			System.out.println("时间戳: " + cell.getTimestamp());
		}
	}

}
