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

    def test_has_egress(self):
        r = ancl.Role("testContextA::testModelA::testComponentA11")
        r.add_egress(ancl.Dependency({
            "name": "testComponentA12::testServiceA12",
        }))
        r.add_egress(ancl.Dependency({
            "name": "testComponentA13::testServiceA13",
        }))
        r.replace_egress(
            ["testContextA::testModelA::testComponentA13","testServiceA13"],
            [
                ["testContextB::testModelB::testComponentB","testServiceB"],
                ["testContextC::testModelC::testComponentC","testServiceC"],
            ]
        )
        # Has regular egress
        self.assertTrue(r.has_egress("testContextA::testModelA::testComponentA12::testServiceA12"))
        # Does not have replaced egress
        self.assertFalse(r.has_egress("testContextA::testModelA::testComponentA13::testServiceA13"))
        # Has egresses that replaced
        self.assertTrue(r.has_egress("testContextB::testModelB::testComponentB::testServiceB"))
        self.assertTrue(r.has_egress("testContextC::testModelC::testComponentC::testServiceC"))
        # Does not have a random egress
        self.assertFalse(r.has_egress("testContextD::testModelD::testComponentD::testServiceD"))

if __name__ == "__main__":
    unittest.main()
