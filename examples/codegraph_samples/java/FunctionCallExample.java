public class FunctionCallExample {
    public static int helperSquareJava(int value) {
        return value * value;
    }

    public static int sumSquaresJava(int[] values) {
        int total = 0;
        for (int value : values) {
            total += helperSquareJava(value);
        }
        return total;
    }
}
