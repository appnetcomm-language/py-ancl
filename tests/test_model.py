import ancl
import unittest

class ModelSyntaxTest(unittest.TestCase):
    def test_syntax_empty_model(self):
        self.assertIsNotNone(ancl.Model.check_syntax({}))

    def test_syntax_missing_components(self):
        self.assertIsNotNone(ancl.Model.check_syntax({
            "name": "testModel",
        }))

    def test_syntax_components_not_array(self):
        self.assertIsNotNone(ancl.Model.check_syntax({
            "name": "testModel",
            "components": 123,
        }))

    def test_syntax_empty_components(self):
        self.assertIsNone(ancl.Model.check_syntax({
            "name": "testModel",
            "components": [],
        }))

    def test_syntax_duplciate_component_names(self):
        self.assertIsNotNone(ancl.Model.check_syntax({
            "name": "testModel",
            "components": [
                { "name": "testDupComp", "ingress": [], "egress": [] },
                { "name": "testDupComp", "ingress": [], "egress": [] },
            ]
        }))

    def test_syntax_valid(self):
        self.assertIsNone(ancl.Model.check_syntax({
            "name": "testModel",
            "components": [
                {
                    "name": "testComponent1",
                    "ingress": [
                        {
                            "name": "testService1",
                            "ports": [ "123-456/udp" ],
                        }
                    ],
                    "egress": [
                        { "name": "testComponent2::testService2" },
                    ]
                }
            ],
        }))

class ModelInitTest(unittest.TestCase):

    def test_init(self):
        m = ancl.Model({
            "name": "testModel",
            "components": [
                {
                    "name": "testComponent1",
                    "ingress": [
                        {
                            "name": "testService11",
                            "ports": [ "123-456/tcp", ],
                        },
                    ],
                    "egress": [
                        { "name": "testComponent2::testService21", },
                    ]
                },
                {
                    "name": "testComponent2",
                    "ingress": [
                        {
                            "name": "testService21",
                            "ports": [ "654-987/udp", ],
                        },
                    ],
                    "egress": [
                        { "name": "testComponent1::testService11", },
                    ],
                },
            ],
        })
        self.assertEqual(m.name, "testModel")
        self.assertEqual(len(m.list_components()),2)
        self.assertEqual(m.component("testComponent2").ingress("testService21").port("654-987/udp"),[654,987,"udp"])
        self.assertEqual(m.service("testComponent2::testService21").port("654-987/udp"),[654,987,"udp"])
        self.assertIsNotNone(m.component("testComponent1").egress("testComponent2::testService21"))
        self.assertIsNotNone(m.dependency("testComponent1::testComponent2::testService21"))

if __name__ == '__main__':
    unittest.main()
