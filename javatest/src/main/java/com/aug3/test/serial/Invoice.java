package com.aug3.test.serial;

import java.io.Externalizable;
import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectOutput;
import java.util.Date;

public final class Invoice implements Externalizable {

	private int invoiceID;
	private Date invoiceDate = null;
	private int invoiceNumber;
	private int customerID;

	public Invoice(final int invoiceID, final int invoiceNumber, final Date invoiceDate, int customerID) {
		this.invoiceID = invoiceID;
		this.invoiceNumber = invoiceNumber;
		this.invoiceDate = (Date) invoiceDate.clone();
		this.customerID = customerID;
	}

	/**
	 * No-argument constructor required by {@link Externalizable}.
	 */
	public Invoice() {
	}

	public int getInvoiceID() {
		return invoiceID;
	}

	public Date getInvoiceDate() {
		return (Date) invoiceDate.clone();
	}

	public void setInvoiceDate(final Date invoiceDate) {
		this.invoiceDate = (Date) invoiceDate.clone();
	}

	public int getInvoiceNumber() {
		return invoiceNumber;
	}

	public void setInvoiceNumber(final int invoiceNumber) {
		this.invoiceNumber = invoiceNumber;
	}

	public void writeExternal(final ObjectOutput out) throws IOException {

		out.writeObject(invoiceDate);
		out.writeInt(invoiceID);
		out.writeInt(invoiceNumber);
		out.writeInt(customerID);
	}

	public void readExternal(final ObjectInput in) throws IOException, ClassNotFoundException {
		invoiceDate = (Date) in.readObject();
		invoiceID = in.readInt();
		invoiceNumber = in.readInt();
		customerID = in.readInt();
	}

	public boolean equals(final Object o) {
		if (this == o)
			return true;
		if (o == null || getClass() != o.getClass())
			return false;
		final Invoice invoice = (Invoice) o;
		if (invoiceID != invoice.invoiceID)
			return false;
		if (invoiceNumber != invoice.invoiceNumber)
			return false;
		if (customerID != invoice.customerID)
			return false;
		if (invoiceDate != null ? !invoiceDate.equals(invoice.invoiceDate) : invoice.invoiceDate != null)
			return false;
		return true;
	}

	public int hashCode() {
		int result = invoiceID;
		result = 31 * result + (invoiceDate != null ? invoiceDate.hashCode() : 0);
		result = 31 * result + invoiceNumber;
		result = 31 * result + customerID;
		return result;
	}

}
