package com.aug3.test.util;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.math.BigInteger;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.security.DigestInputStream;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import org.apache.commons.codec.digest.DigestUtils;

public class MD5Sum {

	public static String md5sum(File file) {
		String value = null;
		FileInputStream in = null;
		try {
			in = new FileInputStream(file);
			MappedByteBuffer byteBuffer = in.getChannel().map(FileChannel.MapMode.READ_ONLY, 0, file.length());
			MessageDigest md5 = MessageDigest.getInstance("MD5");
			md5.update(byteBuffer);
			BigInteger bi = new BigInteger(1, md5.digest());
			value = bi.toString(16);
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if (null != in) {
				try {
					in.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return value;
	}

	public static String getMD5Str(InputStream is) {
		DigestInputStream dis = null;
		try {
			MessageDigest messageDigest = MessageDigest.getInstance("MD5");
			messageDigest.reset();
			dis = new DigestInputStream(is, messageDigest);
			byte[] buffer = new byte[1024 * 200];
			while (dis.read(buffer) != -1) {
				break;
			}
			return new BigInteger(1, messageDigest.digest()).toString(16);
		} catch (Exception e) {
			return "";
		} finally {
			if (dis != null) {
				try {
					dis.close();
				} catch (IOException e) {
				}
			}
		}

	}

	public static String getHash(InputStream is) throws IOException, NoSuchAlgorithmException {

		byte[] buffer = new byte[8192];
		MessageDigest md5 = MessageDigest.getInstance("MD5");

		int len;
		while ((len = is.read(buffer)) != -1) {
			md5.update(buffer, 0, len);
		}

		is.close();
		// 也可以用apache自带的计算MD5方法
		return DigestUtils.md5Hex(md5.digest());
		// 自己写的转计算MD5方法
		// return toHexString(md5.digest());
	}

	private static char[] hexChar = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };

	protected static String toHexString(byte[] b) {
		StringBuilder sb = new StringBuilder(b.length * 2);
		for (int i = 0; i < b.length; i++) {
			sb.append(hexChar[(b[i] & 0xf0) >>> 4]);
			sb.append(hexChar[b[i] & 0x0f]);
		}
		return sb.toString();
	}

	public static void main(String[] args) throws NoSuchAlgorithmException, IOException {

		// File f = new File("D:\\received\\head first python.pdf");
		File f = new File("D:\\b.pdf");
		FileInputStream fis = new FileInputStream(f);

		long t1 = System.currentTimeMillis();
//		System.out.println(MD5Sum.getMD5Str(fis));
		long t2 = System.currentTimeMillis();
		System.out.println(t2 - t1);

		t1 = System.currentTimeMillis();
		// MD5Sum.getHash(fis);
		t2 = System.currentTimeMillis();
		System.out.println(t2 - t1);

		t1 = System.currentTimeMillis();
		System.out.println(MD5Sum.md5sum(f));
		t2 = System.currentTimeMillis();
		System.out.println(t2 - t1);
	}

}
