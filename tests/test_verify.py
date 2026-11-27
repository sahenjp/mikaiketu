import unittest
from itertools import product
from scripts import verify as v


class VerificationTests(unittest.TestCase):
    def test_known_obstructions(self):
        for p, q in v.KNOWN.items():
            self.assertTrue(v.obstructed(v.residues(p, q), q))

    def test_subgroups(self):
        for p in (5, 7, 11, 13, 17, 19):
            for k in range(2, 30, 2):
                q = k*p + 1
                if v.is_prime(q):
                    self.assertEqual(v.subgroup_residues(p, q), v.residues(p, q))

    def test_local7(self):
        cert = v.local7()
        self.assertEqual(len(cert), 28)
        for q, abc in cert.items():
            self.assertTrue(all(a % q for a in abc))
            self.assertEqual(sum(pow(a, 7, q) for a in abc) % q, v.N % q)
        self.assertEqual(v.N % 49, 1)

    def test_p7_mod29(self):
        R = v.residues(7, 29)
        self.assertEqual({t for t in product(R, repeat=3) if sum(t) % 29 == v.N % 29}, {(17, 17, 17)})

    def test_small7(self):
        self.assertEqual(v.small7(), [])
        self.assertGreater(9**7 - 8**7, 7**7 + v.N)
        self.assertGreater(8**7, 2*7**7 + v.N)

    def test_gap_search(self):
        for p, x, d, y in ((7, 10, 1, 15), (19, 20, 2, 30), (7, 9, 2, 10)):
            target = (y+d)**p-y**p
            self.assertEqual(v.find_y(p, x, d, target), y)
            self.assertIsNone(v.find_y(p, x, d, target+1))

    def test_small_search(self):
        for p in (7, 19, 31):
            self.assertIsNone(v.search_exponent(p, 100)[0])


if __name__ == '__main__':
    unittest.main()
