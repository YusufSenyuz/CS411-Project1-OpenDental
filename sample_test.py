import unittest
from unittest.mock import patch, MagicMock
from personnel_dashboard import submit_patient

class TestSubmitPatient(unittest.TestCase):
    @patch("personnel_dashboard.name_entry")
    @patch("personnel_dashboard.age_entry")
    @patch("personnel_dashboard.gender_combobox")
    @patch("personnel_dashboard.race_combobox")
    @patch("personnel_dashboard.education_combobox")
    @patch("personnel_dashboard.email_entry")
    @patch("personnel_dashboard.doctor_combobox")
    @patch("sqlite3.connect")
    @patch("personnel_dashboard.messagebox.showinfo")
    @patch("personnel_dashboard.messagebox.showerror")
    def test_submit_patient_success(self, mock_showerror, mock_showinfo, mock_connect,
                                    mock_doctor_combobox, mock_email_entry, mock_education_combobox,
                                    mock_race_combobox, mock_gender_combobox, mock_age_entry,
                                    mock_name_entry):
        # Simulate user input
        mock_name_entry.get.return_value = "John Doe"
        mock_age_entry.get.return_value = "30"
        mock_gender_combobox.get.return_value = "Male"
        mock_race_combobox.get.return_value = "White"
        mock_education_combobox.get.return_value = "Bachelor's"
        mock_email_entry.get.return_value = "johndoe@example.com"
        mock_doctor_combobox.get.return_value = "Dr. Smith"

        # Mock database connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Call the function under test
        submit_patient()

        # Assertions
        # Verify the SQL query was executed correctly
        mock_cursor.execute.assert_called_with(
            """
            INSERT INTO patients (name, age, gender, race, education_level, email, assigned_doctor)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            ("John Doe", 30, "Male", "White", "Bachelor's", "johndoe@example.com", "Dr. Smith")
        )

        # Verify commit was called
        mock_conn.commit.assert_called_once()

        # Verify success message was displayed
        mock_showinfo.assert_called_with("Success", "Patient added successfully!")
        mock_showerror.assert_not_called()

    @patch("personnel_dashboard.messagebox.showerror")
    @patch("personnel_dashboard.name_entry")
    def test_submit_patient_missing_fields(self, mock_name_entry, mock_showerror):
        # Simulate empty input for required fields
        mock_name_entry.get.return_value = ""  # Name is empty

        # Call the function under test
        submit_patient()

        # Verify that an error message is shown
        mock_showerror.assert_called_with("Input Error", "All fields must be filled!")


if __name__ == "__main__":
    unittest.main()