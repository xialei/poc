package com.aug3.test.io.netty;

import java.net.InetSocketAddress;
import java.util.concurrent.Executors;

import org.jboss.netty.bootstrap.ServerBootstrap;
import org.jboss.netty.buffer.ChannelBuffer;
import org.jboss.netty.buffer.ChannelBuffers;
import org.jboss.netty.channel.Channel;
import org.jboss.netty.channel.ChannelHandlerContext;
import org.jboss.netty.channel.ChannelStateEvent;
import org.jboss.netty.channel.MessageEvent;
import org.jboss.netty.channel.SimpleChannelHandler;
import org.jboss.netty.channel.socket.nio.NioServerSocketChannelFactory;

public class Server {

	ServerBootstrap bootstrap;
	Channel parentChannel;
	InetSocketAddress localAddress;
	MyChannelHandler channelHandler = new MyChannelHandler();

	Server() {
		bootstrap = new ServerBootstrap(new NioServerSocketChannelFactory(Executors.newCachedThreadPool(),
				Executors.newCachedThreadPool()));
		bootstrap.setOption("reuseAddress", true);
		bootstrap.setOption("child.tcpNoDelay", true);
		bootstrap.setOption("child.soLinger", 2);
		bootstrap.getPipeline().addLast("servercnfactory", channelHandler);
	}

	void config(int port) {
		this.localAddress = new InetSocketAddress(port);
	}

	void start() {
		parentChannel = bootstrap.bind(localAddress);
	}

	class MyChannelHandler extends SimpleChannelHandler {

		@Override
		public void channelClosed(ChannelHandlerContext ctx, ChannelStateEvent e) throws Exception {
			System.out.println("Channel closed " + e);
		}

		@Override
		public void channelConnected(ChannelHandlerContext ctx, ChannelStateEvent e) throws Exception {
			System.out.println("Channel connected " + e);
			Channel ch = e.getChannel();
			ChannelBuffer cb = ChannelBuffers.wrappedBuffer("Client connected to server!".getBytes());
			ch.write(cb);
		}

		@Override
		public void messageReceived(ChannelHandlerContext ctx, MessageEvent e) throws Exception {
			try {
				System.out.println("New message " + e.toString() + " from " + ctx.getChannel());

				Channel ch = e.getChannel();
				ch.write(e.getMessage());

			} catch (Exception ex) {
				ex.printStackTrace();
				throw ex;
			}
		}

	}

}
