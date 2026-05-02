package Week_7;

public class LegacyOrderFacade {

    private final LegacyOrderProcessor legacyAgent;

    public LegacyOrderFacade() {
        this.legacyAgent = new LegacyOrderProcessor();
    }

    public void executeOrder(String email, String id, double cost, String destination) {
        legacyAgent.processOrder(email, id, cost, destination);
    }
}
