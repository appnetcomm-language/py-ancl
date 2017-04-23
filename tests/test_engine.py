import ancl
import unittest

class EngineFileTest(unittest.TestCase):
    def test_file(self):
        e = ancl.Engine()
        e.add_file("tests/fixtures/test1.ancl")
        self.assertEqual(e.num_models, 2)
        self.assertIsNotNone(e.model("testModel1"))
        self.assertEqual(e.num_connections,1)
        self.assertIsNotNone(e.connection(ingress="prod::testModel1::testComponent12::testAbstractService"))
        self.assertEqual(e.num_nodes, 2)
        self.assertIsNotNone(e.node("192.0.2.1/32"))

    def test_merge_not_implemented(self):
        e = ancl.Engine()
        with self.assertRaises(ancl.ModelMergeError):
            e.add_file("tests/fixtures/test2a.ancl")
            e.add_file("tests/fixtures/test2b.ancl")

    def test_directory(self):
        e = ancl.Engine()
        e.add_directory("tests/fixtures/engine_test_directory")
        self.assertEqual(e.num_models, 2)
        self.assertEqual(len(e.model("testModelB").list_components()), 2)
        self.assertEqual(e.num_nodes, 3)
        self.assertEqual(e.node("192.0.2.1/32").name, "192.0.2.1/32")
        self.assertIn("subdir::testModelA1::testComponentA11", e.node("192.0.2.50/32").roles)

    def test_render(self):
        e = ancl.Engine()
        e.add_file("tests/fixtures/engine_test_render.ancl")
        e.render()
        # Role Tests
        r1 = e.role("prod::testModel1::testComponent11")
        self.assertIsNotNone(r1)
        self.assertIn(["shared::testModel2::testComponent22","testService"], r1.egresses)
        r3 = e.role("prod::testModel3::testComponent31")
        self.assertIsNotNone(r3)
        self.assertIn(["shared::testModel2::testComponent22","testService"], r3.egresses)
        # Node Tests
        self.assertEqual(e.num_rendered_nodes, 3)
        self.assertIn("shared::testModel2::testComponent22", e.rendered_node("192.0.2.2/32").roles)

    def test_render_grouprole(self):
        e = ancl.Engine()
        e.add_file("tests/fixtures/engine_test_grouprole.ancl")
        e.render()
        self.assertEqual(e.num_groups, 1)
        rg = e.group("prod::grouprole::groupComponent")
        self.assertIsNotNone(rg)
        rn = e.rendered_node("192.0.2.1/32")
        self.assertIn("prod::testModel1::testComponent11", rn.roles)
        self.assertIn("prod::testModel2::testComponent21", rn.roles)

    def test_find_flow(self):
        e = ancl.Engine()
        e.add_file("tests/fixtures/engine_test_render.ancl")
        e.render()
        e.rendered_node("192.0.2.2/32").add_listener(123,"tcp")
        # ingress
        f = e.find_flow(
            "192.0.2.2/32", 123,
            "192.0.2.1/32", 32000,
            "tcp"
        )
        self.assertEqual(len(f),1)
        self.assertEqual("prod::testModel1::testComponent11", f[0][0])
        self.assertEqual(["shared::testModel2::testComponent22","testService"], f[0][1])
        # egress
        f = e.find_flow(
            "192.0.2.1/32", 32000,
            "192.0.2.2/32", 123,
            "tcp"
        )
        self.assertEqual(len(f),1)
        self.assertEqual("prod::testModel1::testComponent11", f[0][0])
        self.assertEqual(["shared::testModel2::testComponent22","testService"], f[0][1])

if __name__ == '__main__':
    unittest.main()
