package com.aug3.test.serial;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.Externalizable;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;

import com.esotericsoftware.kryo.Kryo;
import com.esotericsoftware.kryo.io.Input;
import com.esotericsoftware.kryo.io.Output;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class TestSerial {

	private static Gson gson = new GsonBuilder().serializeNulls().create();
	private static Kryo kryo = new Kryo();

	public static void main(String[] args) throws Exception {

		for (int i = 1; i <= 10; i++) {
			System.out.println("--------------" + i * 200);
			test(i * 200);
		}

	}

	public static void test(int loops) throws Exception {
		Date d = new SimpleDateFormat("yyyy-MM-dd").parse("2011-01-01");
		// test externalizable write
		long t1 = System.currentTimeMillis();

		Invoice inv = new Invoice(1, 2, d, 4);
		byte[][] obj = null;
		for (int i = 0; i < loops; i++) {
			inv.setInvoiceNumber(i+100);
			obj = serializeObject(inv);
		}

		long t2 = System.currentTimeMillis();
		System.out.println("externalizable write : " + (t2 - t1));

		for (int i = 0; i < loops; i++) {
			deserializeObject(obj);
		}

		long t3 = System.currentTimeMillis();
		System.out.println("externalizable read : " + (t3 - t2));

		// ///////////////////////////////////////////

		Invoice1 inv1 = new Invoice1(1, 2, d, 4);
		byte[] buf = null;
		for (int i = 0; i < loops; i++) {
			inv1.setInvoiceNumber(i+100);
			buf = serializeObj(inv1);
		}

		long t4 = System.currentTimeMillis();
		System.out.println("serializable write : " + (t4 - t3));

		for (int i = 0; i < loops; i++) {
			deserializeObject(obj);
		}

		long t5 = System.currentTimeMillis();
		System.out.println("serializable read : " + (t5 - t4));

		// ///////////////////////////////////////////
		String json = null;
		for (int i = 0; i < loops; i++) {
			inv1.setInvoiceNumber(i+100);
			json = gson.toJson(inv1);
		}

		long t6 = System.currentTimeMillis();
		System.out.println("gson write : " + (t6 - t5));

		for (int i = 0; i < loops; i++) {
			gson.fromJson(json, Invoice1.class);
		}
		long t7 = System.currentTimeMillis();
		System.out.println("gson read : " + (t7 - t6));

		// ///////////////////////////////////////////
		for (int i = 0; i < loops; i++) {
			Output output = new Output(new FileOutputStream("file.bin"));
			inv1.setInvoiceNumber(i+100);
			kryo.writeObject(output, inv1);
			output.close();
		}
		long t8 = System.currentTimeMillis();
		System.out.println("kryo write : " + (t8 - t7));

		for (int i = 0; i < loops; i++) {
			Input input = new Input(new FileInputStream("file.bin"));
			Invoice1 someObject = kryo.readObject(input, Invoice1.class);
			input.close();
		}
		long t9 = System.currentTimeMillis();
		System.out.println("kryo read : " + (t9 - t8));
	}

	public static byte[][] serializeObject(Externalizable object) throws Exception {
		ByteArrayOutputStream baos = null;
		ObjectOutputStream oos = null;
		byte[][] res = new byte[2][];

		try {
			baos = new ByteArrayOutputStream();
			oos = new ObjectOutputStream(baos);

			object.writeExternal(oos);
			oos.flush();

			res[0] = object.getClass().getName().getBytes();
			res[1] = baos.toByteArray();

		} catch (Exception ex) {
			throw ex;
		} finally {
			try {
				if (oos != null)
					oos.close();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}

		return res;
	}

	public static Externalizable deserializeObject(byte[][] rowObject) throws Exception {
		ObjectInputStream ois = null;
		String objectClassName = null;
		Externalizable res = null;

		try {

			objectClassName = new String(rowObject[0]);
			byte[] objectBytes = rowObject[1];

			ois = new ObjectInputStream(new ByteArrayInputStream(objectBytes));

			Class objectClass = Class.forName(objectClassName);
			res = (Externalizable) objectClass.newInstance();
			res.readExternal(ois);

		} catch (Exception ex) {
			throw ex;
		} finally {
			try {
				if (ois != null)
					ois.close();
			} catch (Exception e) {
				e.printStackTrace();
			}

		}

		return res;

	}

	public static Object deserializeObj(byte[] buf) throws IOException, ClassNotFoundException {

		Object obj = null;
		if (buf != null) {
			ObjectInputStream ois = null;
			try {
				ois = new ObjectInputStream(new ByteArrayInputStream(buf));
				obj = ois.readObject();
			} catch (IOException e) {
				throw e;
			} catch (ClassNotFoundException e) {
				throw e;
			} finally {
				if (ois != null) {
					try {
						ois.close();
					} catch (IOException e) {
						throw e;
					}
				}
			}
		}

		return obj;
	}

	public static byte[] serializeObj(Object obj) {
		byte[] buf = null;

		if (obj != null) {
			ByteArrayOutputStream baos = new ByteArrayOutputStream();
			ObjectOutputStream oos = null;
			try {
				oos = new ObjectOutputStream(baos);
				oos.writeObject(obj);
				buf = baos.toByteArray();
			} catch (IOException e) {
				e.printStackTrace();
			} finally {
				if (oos != null) {
					try {
						oos.close();
					} catch (IOException e) {
					}
				}
			}
		}

		return buf;

	}

}
