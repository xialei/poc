package com.aug3.test.hadoop;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.URI;

import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class TestHDFS {

	private static Configuration conf = null;

	public static void main(String[] args) throws Exception {

		conf = new Configuration();
		conf.addResource(new Path("./core-site.xml"));
		conf.addResource(new Path("./hdfs-site.xml"));

		copyLocalFileToHdfs("D://architectgen201501.pdf", "/file/architectgen201501.pdf", false);
		byte[] b = readFromFileToByteArray("file:///file/architectgen201501.pdf");
		System.out.println(b.length);
	}

	public static boolean copyLocalFileToHdfs(String fromFile, String toFile, boolean isCheckExist) throws Exception {

		FileSystem fs = null;
		try {
			fs = FileSystem.get(conf);

			Path srcPath = new Path(fromFile); // 原路径
			Path dstPath = new Path(toFile); // 目标路径

			// 首先判断源路径是否存在，和输出路轻是否存在，则存在抛出异常，防止被误覆盖掉
			if (!new File(fromFile).exists()) {
				throw new Exception("要拷贝源文件" + fromFile + ",不存在，请检查!");
			}

			if (isCheckExist) {
				if (fs.exists(dstPath)) {
					System.out.println("要粘贴到的目录" + toFile + ",已存在!");
					return true;
				}
			}

			// 调用文件系统的文件复制函数,前面参数是指是否删除原文件，true为删除，默认为false
			fs.copyFromLocalFile(false, srcPath, dstPath);

			return true;
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			fs.close();
		}

		return false;
	}

	public static byte[] readFromFileToByteArray(String srcFile) throws Exception {

		if (StringUtils.isBlank(srcFile)) {
			throw new Exception("所要读取的源文件" + srcFile + ",不存在，请检查!");
		}
		FileSystem fs = FileSystem.get(conf);
		FSDataInputStream hdfsInStream = fs.open(new Path(srcFile));

		byte[] byteArray = new byte[65536];

		// 存放最后的所有字节数组
		ByteArrayOutputStream bos = new ByteArrayOutputStream();

		// 实际读过来多少
		int readLen = 0;
		while ((readLen = hdfsInStream.read(byteArray)) > 0) {
			bos.write(byteArray);
			byteArray = new byte[65536];
		}

		hdfsInStream.close();

		return bos.toByteArray();
	}

	public static void readFromHdfs(String fromFile, String outputFile) throws Exception {

		FileSystem fs = FileSystem.get(URI.create(fromFile), conf);
		FSDataInputStream hdfsInStream = fs.open(new Path(fromFile));

		OutputStream out = new FileOutputStream(outputFile);
		byte[] ioBuffer = new byte[1024];
		int readLen = hdfsInStream.read(ioBuffer);
		while (-1 != readLen) {
			out.write(ioBuffer, 0, readLen);
			System.out.println(new String(ioBuffer, "utf-8"));
			readLen = hdfsInStream.read(ioBuffer);
		}
		out.close();
		hdfsInStream.close();
	}

	public void deleteFile(String fileName) throws IOException {
		FileSystem fs = FileSystem.get(conf);
		Path f = new Path(fileName);
		boolean isExists = fs.exists(f);
		if (isExists) { // if exists, delete
			boolean isDel = fs.delete(f, true);
			System.out.println(fileName + "  delete? \t" + isDel);
		} else {
			System.out.println(fileName + "  exist? \t" + isExists);
		}
		fs.close();
	}

}
