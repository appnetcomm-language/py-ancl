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
        r1 = e.role("prod::testModel1::testComponent11")
        self.assertIsNotNone(r1)
        self.assertIn(["shared::testModel2::testComponent22","testService"], r1.egresses)
        r3 = e.role("prod::testModel3::testComponent31")
        self.assertIsNotNone(r3)
        self.assertIn(["shared::testModel2::testComponent22","testService"], r3.egresses)

if __name__ == '__main__':
    unittest.main()
