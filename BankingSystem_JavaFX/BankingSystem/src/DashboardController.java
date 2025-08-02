import javafx.fxml.FXML;
import javafx.scene.control.Label;

public class DashboardController {
    @FXML private Label statusLabel;
    private final BankingSystem bank = new BankingSystem();

    @FXML
    private void handleDeposit() {
        bank.deposit(100);
        statusLabel.setText("Deposited ₹100");
    }

    @FXML
    private void handleWithdraw() {
        boolean success = bank.withdraw(50);
        statusLabel.setText(success ? "Withdrew ₹50" : "Insufficient Balance!");
    }

    @FXML
    private void handleViewBalance() {
        statusLabel.setText("Current Balance: ₹" + bank.getBalance());
    }

    @FXML
    private void handleViewTransactions() {
        statusLabel.setText(bank.getLastTransaction());
    }
}
