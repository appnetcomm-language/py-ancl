import ancl
import unittest

class EngineFileTest(unittest.TestCase):
    def test_file(self):
        e = ancl.Engine()
        e.add_file("tests/fixtures/test1.yaml")
        self.assertEqual(e.num_models, 2)
        self.assertIsNotNone(e.model("testModel1"))
        self.assertEqual(e.num_connections,1)
        self.assertIsNotNone(e.connection(ingress="prod::testModel1::testComponent12::testAbstractService"))
        self.assertEqual(e.num_nodes, 2)
        self.assertIsNotNone(e.node("192.0.2.1/32"))

    def test_merge_not_implemented(self):
        e = ancl.Engine()
        with self.assertRaises(ancl.ModelMergeError):
            e.add_file("tests/fixtures/test2a.yaml")
            e.add_file("tests/fixtures/test2b.yaml")

    def test_dir(self):
        pass

if __name__ == '__main__':
    unittest.main()
