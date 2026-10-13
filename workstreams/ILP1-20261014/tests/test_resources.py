import copy
import itertools
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"src"))
from rob import Program,solve
from resources import saturated_window,check_saturation_certificate


class ResourceTests(unittest.TestCase):
    def test_all_forward_dags_through_five(self):
        for n in range(1,6):
            edges=list(itertools.combinations(range(n),2))
            for mask in range(1<<len(edges)):
                p=Program(n,tuple(e for k,e in enumerate(edges) if mask>>k&1))
                cert=saturated_window(p)
                self.assertTrue(check_saturation_certificate(cert)["valid"])
                original=solve(p,n,n)["cycles"]
                b=next(b for b in range(1,n+1) if solve(p,b,n)["cycles"]==original)
                self.assertEqual(cert["B_sat"],b)

    def test_schedule_footprint_is_not_asap_saturation(self):
        cert=saturated_window(Program(3,((0,1),)))
        self.assertEqual(cert["B_sat"],2)
        self.assertEqual(cert["cycles"],2)

    def test_compact_certificate_tamper_controls(self):
        x=saturated_window(Program(4,((1,3),(2,3))))
        self.assertEqual(x["B_sat"],3)
        bad=copy.deepcopy(x); bad["smaller_window_chain"]=bad["smaller_window_chain"][:1]
        with self.assertRaises(ValueError):check_saturation_certificate(bad)
        bad=copy.deepcopy(x);bad["original_critical_chain"]=[0,1]
        with self.assertRaises(ValueError):check_saturation_certificate(bad)
        bad=copy.deepcopy(x);bad["B_sat"]=2
        with self.assertRaises(ValueError):check_saturation_certificate(bad)


if __name__=="__main__":unittest.main()
