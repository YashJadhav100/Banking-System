import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.stage.Stage;

public class LoginController {
    @FXML private TextField usernameField;
    @FXML private PasswordField passwordField;
    @FXML private Label errorLabel;

    @FXML
    private void handleLogin(ActionEvent event) {
        String username = usernameField.getText();
        String password = passwordField.getText();

        if (username.equals("user") && password.equals("pass")) {
            try {
                Parent root = FXMLLoader.load(getClass().getResource("dashboard.fxml"));
                Stage stage = (Stage) usernameField.getScene().getWindow();
                stage.setTitle("Banking Dashboard");
                stage.setScene(new Scene(root));
            } catch (Exception e) {
                errorLabel.setText("Failed to load dashboard.");
            }
        } else {
            errorLabel.setText("Invalid credentials!");
        }
    }
}
