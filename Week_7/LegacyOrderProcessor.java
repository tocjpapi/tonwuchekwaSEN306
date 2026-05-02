package Week_7;


class LegacyOrderProcessor {
    public void processOrder(String customerEmail, String itemCode, double amount, String deliveryAddress) {
        // Hardcoded dependencies inside
        Inventory inv = new Inventory();
        Payment pay = new Payment();
        Shipping ship = new Shipping();
        Email email = new Email();

        if (!inv.checkStock(itemCode)) {
            System.out.println("Out of stock");
            return;
        }
        if (!pay.charge(customerEmail, amount)) {
            System.out.println("Payment fail");
            return;
        }
        inv.reserve(itemCode);
        String label = ship.createLabel(deliveryAddress);
        ship.schedulePickup(label);
        email.send(customerEmail, "Order", "Shipped");
        System.out.println("Order complete");
    }
}


class Inventory {
    boolean checkStock(String productId) { return true; }
    void reserve(String productId) { System.out.println("Reserved " + productId); }
}

class Payment {
    boolean charge(String userId, double amount) { return true; }
}

class Shipping {
    String createLabel(String address) { return "TRK-" + System.currentTimeMillis(); }
    void schedulePickup(String label) { System.out.println("Pickup scheduled: " + label); }
}

class Email {
    void send(String to, String subject, String body) {
        System.out.println("Email to " + to + ": " + subject);
    }
}

