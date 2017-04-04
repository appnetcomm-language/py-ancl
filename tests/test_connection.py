import ancl
import unittest

class ConnectionSyntaxTest(unittest.TestCase):
    def test_syntax_empty_connection(self):
        self.assertIsNotNone(ancl.Connection.check_syntax({}))

    def test_syntax_confused_formed(self):
        self.assertIsNotNone(ancl.Connection.check_syntax({
            "ingress": "Context1::Model1::Component1::Ingress1",
            "egress": "Context1::Model1::Component1::Component2::Ingress2",
        }))

    def test_syntax_ingress_bad_form(self):
        self.assertIsNotNone(ancl.Connection.check_syntax({
            "ingress": 123,
            "with": "Context2::Model2::Component2::Ingress2",
        }))
        self.assertIsNotNone(ancl.Connection.check_syntax({
            "ingress": "123",
            "with": "Context2::Model2::Component2::Ingress2",
        }))

    def test_syntax_egress_bad_form(self):
        self.assertIsNotNone(ancl.Connection.check_syntax({
            "egress": 123,
            "with":   "Context3::Model3::Component3::Component4::Ingress4",
        }))
        self.assertIsNotNone(ancl.Connection.check_syntax({
            "egress": "123",
            "with":   "Context3::Model3::Component3::Component4::Ingress4",
        }))

    def test_syntax_missing_with(self):
        self.assertIsNotNone(ancl.Connection.check_syntax({
            "ingress": "Context1::Model1::Component1::Ingress1",
        }))
        self.assertIsNotNone(ancl.Connection.check_syntax({
            "egress": "Context1::Model1::Component1::Component2::Ingress2",
        }))

    def test_syntax_bad_with_form(self):
        self.assertIsNotNone(ancl.Connection.check_syntax({
            "ingress": "Context1::Model1::Component1::Ingress1",
            "with":    123,
        }))
        self.assertIsNotNone(ancl.Connection.check_syntax({
            "egress": "Context1::Model1::Component1::Component2::Ingress2",
            "with":   123,
        }))

    def test_syntax_mismatch_with(self):
        self.assertIsNotNone(ancl.Connection.check_syntax({
            "ingress": "Context1::Model1::Component1::Ingress1",
            "with":    "Context3::Model3::Component3::Component4::Ingress4",
        }))
        self.assertIsNotNone(ancl.Connection.check_syntax({
            "egress": "Context1::Model1::Component1::Component2::Ingress2",
            "with":   "Context2::Model2::Component2::Ingress2",
        }))

    def test_syntax_valid_form(self):
        self.assertIsNone(ancl.Connection.check_syntax({
            "ingress": "Context1::Model1::Component1::Ingress1",
            "with":    [
                        "Context2::Model2::Component2::Ingress2",
                        "Context3::Model3::Component3::Ingress3",
                       ],
        }))
        self.assertIsNone(ancl.Connection.check_syntax({
            "egress": "Context1::Model1::Component1::Component2::Ingress2",
            "with":   [
                       "Context3::Model3::Component3::Component4::Ingress4",
                       "Context5::Model5::Component5::Component6::Ingress6",
                      ],
        }))

class ConnectionInitTest(unittest.TestCase):

    def test_init_ingress(self):
        i = ancl.Connection({
            "ingress": "Context1::Model1::Component1::Ingress1",
            "with":    ["Context2::Model2::Component2::Ingress2"],
        })
        self.assertEqual(i.direction, "ingress")
        self.assertTrue(i.is_ingress())
        self.assertFalse(i.is_egress())
        self.assertEqual(i.src, "Context1::Model1::Component1::Ingress1")
        self.assertEqual(i.dst, ["Context2::Model2::Component2::Ingress2"])

    def test_init_egress(self):
        e = ancl.Connection({
            "egress": "Context1::Model1::Component1::Component2::Ingress2",
            "with":   ["Context3::Model3::Component3::Component4::Ingress4"],
        })
        self.assertEqual(e.direction, "egress")
        self.assertTrue(e.is_egress())
        self.assertFalse(e.is_ingress())
        self.assertEqual(e.src, "Context1::Model1::Component1::Component2::Ingress2")
        self.assertEqual(e.dst, ["Context3::Model3::Component3::Component4::Ingress4"])

if __name__ == '__main__':
    unittest.main()
