public class Fib {

    static int fib(int n) {
        if (n < 2) {
            return n;
        }
        return fib(n - 1) + fib(n - 2);
    }

    public static void main(String[] args) {
        for (int i = 0; i <= 20; i++) {
            System.out.print(fib(i));
            System.out.print(' ');
        }
        System.out.println();
    }
}
