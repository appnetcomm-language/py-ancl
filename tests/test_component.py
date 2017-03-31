import ancl
import unittest

class ComponentSyntaxTest(unittest.TestCase):

    def test_syntax_component_missing_name(self):
        self.assertIsNotNone(ancl.Component.check_syntax({}))
        # with self.assertRaises(ancl.ComponentSyntaxError):
        #     ancl.Component.check_syntax({})

    def test_syntax_component_bad_name(self):
        # with self.assertRaises(ancl.ComponentSyntaxError):
        self.assertIsNotNone(ancl.Component.check_syntax({
            "name": 123,
        }))

    def test_syntax_component_bad_ingress(self):
        self.assertIsNotNone(ancl.Component.check_syntax({
            "name": "testComponent",
            "ingress": 123,
        }))
        self.assertIsNotNone(ancl.Component.check_syntax({
            "name": "testComponent",
            "ingress": [
                { "badservice": "foo" }
            ]
        }))

    def test_syntax_component_duplicate(self):
        self.assertIsNotNone(ancl.Component.check_syntax({
            "name": "testComponent",
            "ingress": [
                { "name": "dupService", },
                { "name": "dupService", },
            ],
            "egress": [],
        }))
        self.assertIsNotNone(ancl.Component.check_syntax({
            "name": "testComponent",
            "ingress": [],
            "egress": [
                { "name": "dupComp::dupService", },
                { "name": "dupComp::dupService", },
            ],
        }))

    def test_syntax_component_bad_egress(self):
        self.assertIsNotNone(ancl.Component.check_syntax({
            "name": "testComponent",
            "ingress": [],
            "egress": 123,
        }))
        self.assertIsNotNone(ancl.Component.check_syntax({
            "name": "testComponent",
            "ingress": [],
            "egress": [
                123
            ],
        }))
        self.assertIsNotNone(ancl.Component.check_syntax({
            "name": "testComponent",
            "ingress": [],
            "egress": [
                { "baddependency": "foo" }
            ],
        }))

    def test_syntax_valid(self):
        self.assertIsNone(ancl.Component.check_syntax({
            "name": "testComponent1",
            "ingress": [
                { "name": "testService11", "ports": [ "123-456/tcp", ], },
                { "name": "abstractService12", }
            ],
            "egress": [
                { "name": "testComponent2::testService21"},
                { "name": "testComponent3::testService31"},
            ],
        }))

class ComponentInitTest(unittest.TestCase):

    def test_init(self):
        c = ancl.Component({
            "name": "testComponent",
            "ingress": [
                { "name": "testService11", "ports": [ "123-456/tcp", ], },
                { "name": "abstractService12", },
            ],
            "egress": [
                { "name": "testComponent2::testService21", },
                { "name": "testComponent3::testService31", },
            ],
        })
        self.assertEqual(c.name, "testComponent")
        self.assertEqual(len(c.list_ingress()), 2)
        self.assertEqual(c.ingress("testService11").port("123-456/tcp"), [123,456,"tcp"])
        self.assertTrue(c.ingress("abstractService12"))
        self.assertIsNone(c.ingress("notService"))
        self.assertIn("testComponent3::testService31", c.list_egress())
        self.assertEqual(c.egress("testComponent3::testService31").name, "testComponent3::testService31")

if __name__ == '__main__':
    unittest.main()
