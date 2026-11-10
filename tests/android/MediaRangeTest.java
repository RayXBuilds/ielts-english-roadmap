import com.rayxbuilds.stepwise.MediaRange;
import com.rayxbuilds.stepwise.LimitedInputStream;
import java.io.ByteArrayInputStream;
import java.util.Arrays;

public class MediaRangeTest {
    private static void check(String range, long start, long end) {
        if (!Arrays.equals(MediaRange.parse(range, 100), new long[]{start, end})) {
            throw new AssertionError(range);
        }
    }
    public static void main(String[] args) throws Exception {
        check(null, 0, 99);
        check("bytes=10-20", 10, 20);
        check("bytes=50-", 50, 99);
        check("bytes=-10", 90, 99);
        check("bytes=-200", 0, 99);
        check("bytes=10-999", 10, 99);
        for (String bad : new String[]{"bytes=", "bytes=-", "bytes=-0", "bytes=20-10", "bytes=100-", "bytes=1-2,4-5", "bytes=999999999999999999999-"}) {
            try { MediaRange.parse(bad, 100); throw new AssertionError("Accepted " + bad); }
            catch (IllegalArgumentException expected) { }
        }
        LimitedInputStream stream = new LimitedInputStream(new ByteArrayInputStream(new byte[]{1,2,3,4}), 2);
        if (stream.read() != 1 || stream.read(new byte[8]) != 1 || stream.read() != -1) throw new AssertionError("Range leaked");
        stream.close();
        System.out.println("Media ranges and bounded streams passed");
    }
}
