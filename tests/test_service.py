import ancl
import unittest

class ServiceSyntaxTest(unittest.TestCase):

    def test_syntax_service_missing_name(self):
        self.assertIsNotNone(ancl.Service.check_syntax({}))

    def test_syntax_service_bad_ports(self):
        self.assertIsNotNone(ancl.Service.check_syntax({
            "name": "testService1",
            "ports": 123,
        }))
        self.assertIsNotNone(ancl.Service.check_syntax({
            "name": "testService1",
            "ports": [ 123 ],
        }))
        self.assertIsNotNone(ancl.Service.check_syntax({
            "name": "testService1",
            "ports": [ "123" ],
        }))

    def test_syntax_valid(self):
        self.assertIsNone(ancl.Service.check_syntax({
            "name": "testService1",
            "ports": [ "123-456/tcp", ],
        }))

class ServiceInitTest(unittest.TestCase):

    def test_init(self):
        s = ancl.Service({
            "name": "testService",
            "ports": [ "123-456/tcp", ],
        })
        self.assertEqual(s.name, "testService")
        self.assertEqual(s.ports, ["123-456/tcp"])
        self.assertEqual(s.port("123-456/tcp"), [123,456,"tcp"])
        self.assertIsNone(s.port("123-123/tcp"))

    def test_init_abstract(self):
        s = ancl.Service({
            "name": "testService",
        })
        self.assertEqual(s.name, "testService")
        self.assertTrue(s.abstract)

if __name__ == '__main__':
    unittest.main()
