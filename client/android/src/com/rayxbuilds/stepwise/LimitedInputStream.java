package com.rayxbuilds.stepwise;

import java.io.FilterInputStream;
import java.io.IOException;
import java.io.InputStream;

/** Close the underlying asset and stop exactly at the requested media range. */
public final class LimitedInputStream extends FilterInputStream {
    private long remaining;
    public LimitedInputStream(InputStream input, long length) { super(input); remaining = length; }
    @Override public int read() throws IOException {
        if (remaining == 0) return -1;
        int value = in.read();
        if (value != -1) remaining--;
        return value;
    }
    @Override public int read(byte[] buffer, int offset, int length) throws IOException {
        if (length == 0) return 0;
        if (remaining == 0) return -1;
        int count = in.read(buffer, offset, (int) Math.min(length, remaining));
        if (count > 0) remaining -= count;
        return count;
    }
    @Override public long skip(long count) throws IOException {
        long skipped = in.skip(Math.min(count, remaining)); remaining -= skipped; return skipped;
    }
    @Override public int available() throws IOException { return (int) Math.min(in.available(), remaining); }
}
