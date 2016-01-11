package com.aug3.test.hbase;

import java.io.IOException;
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.MasterNotRunningException;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.HBaseAdmin;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Put;

import com.aug3.test.util.DateUtil;
import com.google.protobuf.ServiceException;

public class EquityPriceTransport {

	private final static String tableName = "equity_price";
	private final static String familyName = "hq";

	private final static String QUERYSQL = "select * from equity_price_bak limit ?,?";
	private final static String COUNTSQL = "select count(1) from equity_price_bak";
	private final static int PAGESIZE = 10000;

	// 驱动程序名
	private final static String driver = "com.mysql.jdbc.Driver";

	// URL指向要访问的数据库名scutcs
	private final static String url = "jdbc:mysql://192.168.250.208:3306/ada-fd";

	// private static void
	public static void main(String[] args) throws IOException {
		mysql2hbase();
	}

	private static void mysql2hbase() throws IOException {

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

		// 创建表
		HBaseAdmin admin = new HBaseAdmin(conf);

		if (!admin.tableExists(tableName)) {

			System.out.println("----------start to create table " + tableName);
			HTableDescriptor tableDesc = new HTableDescriptor(TableName.valueOf(tableName));
			tableDesc.addFamily(new HColumnDescriptor(familyName));
			admin.createTable(tableDesc);
		}

		admin.close();

		// 插入表数据
		HTable table = new HTable(conf, tableName);

		// 多条插入
		List<Put> list = new ArrayList<Put>(PAGESIZE);

		Connection conn = null;
		ResultSet rs = null;

		try {
			// 加载驱动程序
			Class.forName(driver);

			// 连续数据库
			conn = DriverManager.getConnection(url, "ada_user", "ada_user");

			System.out.println("----------start to count table " + tableName);
			Statement sts = conn.createStatement();
			rs = sts.executeQuery(COUNTSQL);
			long total = 0;
			if (rs.next()) {
				total = rs.getInt(1);
				total = total / PAGESIZE + 1;
			} else {
				return;
			}

			long t = System.currentTimeMillis();
			System.out.println("----------begin transfer job-----------");

			// statement用来执行SQL语句
			PreparedStatement ps = conn.prepareStatement(QUERYSQL);

			BigDecimal tmp = null;

			for (int page = 0; page <= total; page++) {

				System.out.println(">> p" + (page + 1) + "\t time cost:" + (System.currentTimeMillis() - t));

				ps.setInt(1, page * PAGESIZE + 1);
				ps.setInt(2, PAGESIZE);

				// 结果集
				rs = ps.executeQuery();

				while (rs.next()) {

					// 选择sname这列数据
					String tik = rs.getString("ticker");
					String date = DateUtil.formatDate(rs.getDate("trade_date"));
					long dt = Long.MAX_VALUE - rs.getDate("trade_date").getTime();
					String secu = rs.getString("secu_code");
					String vol = Long.toString(rs.getLong("volume"));
					tmp = rs.getBigDecimal("open_price");
					String op = tmp != null ? tmp.toString() : "";
					String cp = rs.getBigDecimal("close_price").toString();
					String cur = rs.getString("currency");
					tmp = rs.getBigDecimal("turnover_ratio");
					String tor = tmp != null ? tmp.toString() : "";

					byte[] rowkey = (secu + ":" + dt).getBytes();

					list.add(addFields(rowkey, familyName.getBytes(), tik, date, vol, op, cp, cur, tor));
				}

				table.put(list);
				list.clear();

			}

		} catch (ClassNotFoundException e) {

			System.out.println("Sorry,can`t find the Driver!");
			e.printStackTrace();

		} catch (SQLException e) {

			e.printStackTrace();

		} catch (Exception e) {

			e.printStackTrace();

		} finally {
			try {
				rs.close();
			} catch (SQLException e) {
				rs = null;
			}
			try {
				conn.close();
			} catch (SQLException e) {
				conn = null;
			}

			table.close();
		}
	}

	private static Put addFields(byte[] rowkey, byte[] cf, String tik, String date, String volume, String openPrice,
			String closePrice, String cur, String turnOverRate) {

		Put p = null;
		p = new Put(rowkey);
		p.add(cf, "tik".getBytes(), tik.getBytes());
		p.add(cf, "d".getBytes(), date.getBytes());
		p.add(cf, "v".getBytes(), volume.getBytes());
		p.add(cf, "op".getBytes(), openPrice.getBytes());
		p.add(cf, "cp".getBytes(), closePrice.getBytes());
		p.add(cf, "cur".getBytes(), cur.getBytes());
		p.add(cf, "tor".getBytes(), turnOverRate.getBytes());

		return p;
	}

}
