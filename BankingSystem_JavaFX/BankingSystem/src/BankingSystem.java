import java.io.*;
import java.util.*;

public class BankingSystem {
    private final String balanceFile = "balance.txt";
    private final String transactionFile = "transactions.txt";

    public double getBalance() {
        try (BufferedReader br = new BufferedReader(new FileReader(balanceFile))) {
            return Double.parseDouble(br.readLine());
        } catch (IOException e) {
            return 0;
        }
    }

    public void deposit(double amount) {
        double current = getBalance() + amount;
        saveBalance(current);
        logTransaction("Deposit", amount, current);
    }

    public boolean withdraw(double amount) {
        double current = getBalance();
        if (amount > current) return false;
        current -= amount;
        saveBalance(current);
        logTransaction("Withdraw", amount, current);
        return true;
    }

    public String getLastTransaction() {
        try (BufferedReader br = new BufferedReader(new FileReader(transactionFile))) {
            String line, last = "";
            while ((line = br.readLine()) != null) last = line;
            return last;
        } catch (IOException e) {
            return "No transactions yet.";
        }
    }

    private void saveBalance(double balance) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(balanceFile))) {
            bw.write(String.valueOf(balance));
        } catch (IOException ignored) {}
    }

    private void logTransaction(String type, double amount, double balance) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(transactionFile, true))) {
            bw.write(type + " of ₹" + amount + " | Balance: ₹" + balance + " | Time: " + new Date() + "\n");
        } catch (IOException ignored) {}
    }
}
