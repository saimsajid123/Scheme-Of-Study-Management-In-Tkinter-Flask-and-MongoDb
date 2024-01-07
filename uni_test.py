import unittest
from restapi_flask import app, sos_collection

class TestSchemeOfStudyApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.test_db = sos_collection

    def tearDown(self):
        self.test_db.delete_many({})

    def test_remove_item(self):
        self.test_db.update_one(
            {'semester': 'Semester 1'},
            {'$push': {'courses': 'Test Subject: Test Description (TEST123, Test Teacher)'}}
        )

        result_after_update = self.test_db.find_one({'semester': 'Semester 1'}, {'_id': 0, 'courses': 1})
        print("After update:", result_after_update)

        response = self.app.delete('/sos?selected_item=Test Subject: Test Description (TEST123, Test Teacher)')
        self.assertEqual(response.status_code, 200)

        result_after_deletion = self.test_db.find_one({'semester': 'Semester 1'}, {'_id': 0, 'courses': 1})
        print("After deletion:", result_after_deletion)

        self.assertIsNotNone(result_after_update)
        self.assertIsNotNone(result_after_deletion)
        self.assertEqual(len(result_after_deletion['courses']), 0)  # Check for empty 'courses' list
        self.assertNotIn('Test Subject', result_after_deletion.get('courses', []))  # Check that the item is not present

if __name__ == '__main__':
    unittest.main()
