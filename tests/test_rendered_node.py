import ancl
import unittest

class RenderedNodeTest(unittest.TestCase):

    def test_name(self):
        e = ancl.Engine()
        e.add_file("tests/fixtures/engine_test_render.ancl")
        n = e.node("192.0.2.2/32")
        rn = ancl.RenderedNode(n,e)
        self.assertEqual(rn.name,"192.0.2.2/32")

    def test_roles(self):
        e = ancl.Engine()
        e.add_file("tests/fixtures/engine_test_render.ancl")
        e._render_roles()
        e._render_connections()
        n = e.node("192.0.2.2/32")
        rn = ancl.RenderedNode(n,e)
        self.assertTrue(rn.has_role("shared::testModel2::testComponent22"))
        self.assertIsNotNone(rn.role("shared::testModel2::testComponent22"))
        self.assertEqual(rn.role("shared::testModel2::testComponent22"),
                         e.role("shared::testModel2::testComponent22"))

    def test_listener(self):
        e = ancl.Engine()
        e.add_file("tests/fixtures/engine_test_render.ancl")
        n = e.node("192.0.2.2/32")
        rn = ancl.RenderedNode(n,e)
        rn.add_listener(123,"tcp")
        self.assertTrue(rn.has_listener(123,"tcp"))

    def test_ingress(self):
        e = ancl.Engine()
        e.add_file("tests/fixtures/engine_test_render.ancl")
        e._render_roles()
        e._render_connections()
        n = e.node("192.0.2.2/32")
        rn = ancl.RenderedNode(n,e)
        self.assertFalse(rn.has_ingress("wontmatchthis", "dummyservice"))
        self.assertTrue(rn.has_ingress("shared::testModel2::testComponent22", "testService"))
        i = rn.find_ingress_by_port(123,"tcp")
        self.assertEqual(len(i), 1)
        self.assertEqual(i[0], ["shared::testModel2::testComponent22", "testService"])

    def test_egress(self):
        e = ancl.Engine()
        e.add_file("tests/fixtures/engine_test_render.ancl")
        e._render_roles()
        e._render_connections()
        n = e.node("192.0.2.1/32")
        rn = ancl.RenderedNode(n,e)
        self.assertFalse(rn.has_egress("wontmatch","wontmatch"))
        self.assertTrue(rn.has_egress("shared::testModel2::testComponent22", "testService"))
        self.assertIn(["shared::testModel2::testComponent22","testService"],rn.egresses)
        es = rn.roles_with_egress("shared::testModel2::testComponent22","testService")
        self.assertEqual(len(es),1)
        self.assertIn("prod::testModel1::testComponent11", es)

if __name__ == '__main__':
    unittest.main()
