import ancl
import unittest

class DependencySyntaxTest(unittest.TestCase):

    def test_syntax_dependency_missing_name(self):
        self.assertIsNotNone(ancl.Dependency.check_syntax({}))

    def test_syntax_dependency_bad_form(self):
        self.assertIsNotNone(ancl.Dependency.check_syntax({
            "name": 123,
        }))
        self.assertIsNotNone(ancl.Dependency.check_syntax({
            "name": "123",
        }))

    def test_syntax_valid(self):
        self.assertIsNone(ancl.Dependency.check_syntax({
            "name": "testComponent::testService",
        }))

class DependencyInitTest(unittest.TestCase):

    def test_init(self):
        d = ancl.Dependency({"name": "testComponent::testService"})
        self.assertEqual(d.name, "testComponent::testService" )

if __name__ == '__main__':
    unittest.main()
