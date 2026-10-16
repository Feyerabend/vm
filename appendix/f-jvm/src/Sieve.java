public class Sieve {

    public static void main(String[] args) {
        int n = 100;
        int[] composite = new int[n + 1];
        for (int p = 2; p * p <= n; p++) {
            if (composite[p] == 0) {
                for (int k = p * p; k <= n; k += p) {
                    composite[k] = 1;
                }
            }
        }
        int count = 0;
        for (int p = 2; p <= n; p++) {
            if (composite[p] == 0) {
                System.out.print(p);
                System.out.print(' ');
                count++;
            }
        }
        System.out.println();
        System.out.println("primes up to 100:");
        System.out.println(count);
    }
}
