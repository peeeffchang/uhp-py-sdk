import unittest
from uhp.enums.visibility import VisibilityLevel

class TestVisibilityEnum(unittest.TestCase):

    def test_visibility_level_has_correct_members(self):
        expected_members = ["PUBLIC", "PRIVATE", "ANONYMIZED", "RESTRICTED"]
        for member in expected_members:
            self.assertIn(member, VisibilityLevel.__members__)

if __name__ == '__main__':
    unittest.main()
