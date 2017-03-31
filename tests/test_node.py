import ancl
import unittest

class NodeSyntaxTest(unittest.TestCase):
    def test_syntax_empty_model(self):
        self.assertIsNotNone(ancl.Node.check_syntax({}))

    def test_syntax_missing_roles(self):
        self.assertIsNotNone(ancl.Node.check_syntax({
            "name": "testNode"
        }))

    def test_syntax_bad_roles(self):
        self.assertIsNotNone(ancl.Node.check_syntax({
            "name": "testNode",
            "roles": 123
        }))

    def test_syntax_bad_role(self):
        self.assertIsNotNone(ancl.Node.check_syntax({
            "name": "testNode",
            "roles": [ 123 ]
        }))
        self.assertIsNotNone(ancl.Node.check_syntax({
            "name": "testNode",
            "roles": [ "123" ]
        }))

    def test_syntax_valid_form(self):
        self.assertIsNone(ancl.Node.check_syntax({
            "name": "testNode",
            "alias": "test.node.fqdn",
            "roles": [
                "Context1::Model1::Component1",
                "Context2::Model2::Component2",
                "Context3::Model3::Component3",
            ]
        }))

class NodeInitTest(unittest.TestCase):
    def test_init(self):
        n = ancl.Node({
            "name": "testNode",
            "roles": [
                "Context1::Model1::Component1",
                "Context2::Model2::Component2",
                "Context3::Model3::Component3",
            ]
        })
        self.assertEqual(n.name, "testNode")
        self.assertEqual(len(n.roles), 3)
        self.assertIn("Context3::Model3::Component3",n.roles)
        self.assertTrue(n.has_role("Context2::Model2::Component2"))
        self.assertFalse(n.has_role("ContextNot::ModelNot::ComponentNot"))

if __name__ == '__main__':
    unittest.main()
