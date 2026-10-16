public class Divide {

    static int share(int total, int people) {
        return total / people;
    }

    public static void main(String[] args) {
        System.out.println("100 shared by 3, 2, 1 and 0:");
        for (int people = 3; people >= 0; people--) {
            System.out.println(share(100, people));
        }
        System.out.println("never printed");
    }
}
