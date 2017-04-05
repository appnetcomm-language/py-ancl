import ancl
import unittest

class FindTest(unittest.TestCase):

    def test_find_by_ingress(self):
        r = ancl.Role("testContext::testModel::testComponent")
        r.add_ingress(ancl.Service({
            "name": "testService1",
            "ports": [ "100-200/tcp", "400-500/tcp" ],
        }))
        r.add_ingress(ancl.Service({
            "name": "testService2",
            "ports": [ "250/tcp" ],
        }))
        self.assertEqual(r.find_ingress_by_port(123,"tcp"),
                         "testContext::testModel::testComponent::testService1")
        self.assertEqual(r.find_ingress_by_port(450,"tcp"),
                         "testContext::testModel::testComponent::testService1")
        self.assertEqual(r.find_ingress_by_port(250,"tcp"),
                         "testContext::testModel::testComponent::testService2")
        self.assertIsNone(r.find_ingress_by_port(201,"tcp"))

if __name__ == "__main__":
    unittest.main()
