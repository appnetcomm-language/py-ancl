import ancl
import unittest

class GroupRoleTest(unittest.TestCase):

    def test_syntax_empty_model(self):
        self.assertIsNotNone(ancl.GroupRole.check_syntax({}))

    def test_syntax_invalid_name(self):
        self.assertIsNotNone(ancl.GroupRole.check_syntax({
            "name": "foobar"
        }))

    def test_syntax_missing_components(self):
        self.assertIsNotNone(ancl.GroupRole.check_syntax({
            "name": "a::b::c"
        }))

    def test_grouprole_syntax(self):
        pass

    def test_grouprole(self):
        g = ancl.GroupRole({
            "name": "prod::grouprole::testComponent11",
            "roles": [
                    "prod::Model1::testComponent11",
                    "prod::Model2::testComponent21",
            ],
        })
        self.assertEqual(g.name, "prod::grouprole::testComponent11")
        self.assertIn("prod::Model1::testComponent11", g.roles)
        self.assertIn("prod::Model2::testComponent21", g.roles)

if __name__ == "__main__":
    unittest.main()
