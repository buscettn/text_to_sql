import unittest
from semantic_layer.providers.domain_mapping import get_domain

class TestSemanticLayer(unittest.TestCase):
    def test_get_domain_profit(self):
        # Query about profit should map to DOMAIN4 (Profit and Loss)
        domain = get_domain("Tell me about profit and loss statements")
        print(f"Query: 'Tell me about profit and loss statements' -> Domain: {domain}")
        self.assertEqual(domain, "DOMAIN4")

    def test_get_domain_credit(self):
        # Query about credit should map to DOMAIN1 or DOMAIN3
        domain = get_domain("I need information about credit data")
        print(f"Query: 'I need information about credit data' -> Domain: {domain}")
        self.assertIn(domain, ["DOMAIN1", "DOMAIN3"])

    def test_get_domain_securities(self):
        # Query about securities should map to DOMAIN2
        domain = get_domain("Show me the securities transactions")
        print(f"Query: 'Show me the securities transactions' -> Domain: {domain}")
        self.assertEqual(domain, "DOMAIN2")

if __name__ == "__main__":
    unittest.main()
