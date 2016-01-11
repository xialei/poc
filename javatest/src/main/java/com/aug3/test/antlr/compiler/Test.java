package com.aug3.test.antlr.compiler;

import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;

public class Test {
	public static void main(String[] args) throws Exception {

		String[] testStr = { "100+2*34", "(10-1)/3", "5 + (6 * 3)" };

		for (String s : testStr) {
			System.out.println("Input expr: " + s);
			run(s);
		}

	}

	public static void run(String expr) throws Exception {

		ANTLRInputStream input = new ANTLRInputStream(expr);

		ExprLexer lexer = new ExprLexer(input);

		CommonTokenStream tokens = new CommonTokenStream(lexer);

		ExprParser parser = new ExprParser(tokens);

		parser.prog();
		
	}
}
