package Week_7.Exercise_1;

// code refactored

public class BookingFacade {
    private RoomService rooms;
    private PaymentService payment;
    private LoyaltyPoints loyalty;
    private EmailService email;

    public BookingFacade() {
        this.rooms = new RoomService();
        this.payment = new PaymentService();
        this.loyalty = new LoyaltyPoints();
        this.email = new EmailService();
    }

    public boolean bookRoom(String guest, String roomType, double price) {
        if (!rooms.isAvailable(roomType))
            return false;
        if (!payment.charge(guest, price))
            return false;

        rooms.book(roomType, guest);
        loyalty.addPoints(guest, (int) price);
        email.sendConfirmation(guest, roomType);
        return true;
    }

    public static void main(String[] args) {
        BookingFacade booking = new BookingFacade();
        System.out.println(booking.bookRoom("john@example.com", "DELUXE", 250.00));
    }
}

class RoomService {
    void book(String roomtype, String guest) {
    }

    boolean isAvailable(String roomtype) {
        return true;
    }
}

class PaymentService {
    boolean charge(String guest, double price) {
        return true;
    }
}

class LoyaltyPoints {
    boolean addPoints(String guest, int price) {
        return true;
    }
}

class EmailService {
    void sendConfirmation(String guest, String roomtype) {
    }
}