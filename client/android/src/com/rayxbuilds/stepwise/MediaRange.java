package com.rayxbuilds.stepwise;

/** Single HTTP byte ranges used by Android's media player. */
public final class MediaRange {
    private MediaRange() { }
    public static long[] parse(String range, long total) {
        if (total <= 0) throw new IllegalArgumentException("Empty media");
        if (range == null) return new long[]{0, total - 1};
        if (!range.matches("bytes=\\d*-\\d*")) throw new IllegalArgumentException("Invalid range");
        String[] parts = range.substring(6).split("-", -1);
        try {
            if (parts[0].isEmpty()) {
                long suffix = Long.parseLong(parts[1]);
                if (suffix <= 0) throw new IllegalArgumentException("Invalid suffix");
                return new long[]{Math.max(0, total - suffix), total - 1};
            }
            long start = Long.parseLong(parts[0]);
            long end = parts[1].isEmpty() ? total - 1 : Math.min(Long.parseLong(parts[1]), total - 1);
            if (start > end || start >= total) throw new IllegalArgumentException("Outside file");
            return new long[]{start, end};
        } catch (NumberFormatException error) { throw new IllegalArgumentException("Invalid number", error); }
    }
}
