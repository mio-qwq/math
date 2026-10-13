"""Semantic tests, certificate tamper controls, and exact boundary cases."""
import copy
import pathlib
import sys
import unittest

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"src"))
from rob import Program, solve, greedy, earliest_times, required_window, schedule_times
from checker import replay, check_certificate


class ModelTests(unittest.TestCase):
    def test_empty_single_and_invalid_parameters(self):
        for b in (1,2,5):
            for w in (1,2,8):
                empty = solve(Program(0),b,w,True)
                self.assertEqual(check_certificate(empty)["optimum"],0)
                self.assertIsNone(empty["ipc"])
                self.assertEqual(solve(Program(1),b,w)["cycles"],1)
        for n,e in ((-1,()),(2,((1,0),)),(2,((0,2),)),(2,((1,1),))):
            with self.assertRaises(ValueError): Program(n,e)
        for b,w in ((0,1),(1,0),(-1,1),(True,2)):
            with self.assertRaises(ValueError): solve(Program(0),b,w)

    def test_independent_and_serial(self):
        for n in range(1,10):
            for b in range(1,n+2):
                for w in (1,2,3,n+2):
                    independent = solve(Program(n),b,w,True)
                    self.assertEqual(independent["cycles"],(n+min(b,w)-1)//min(b,w))
                    self.assertTrue(check_certificate(independent)["valid"])
                    chain = Program(n,tuple((i,i+1) for i in range(n-1)))
                    self.assertEqual(solve(chain,b,w)["cycles"],n)

    def test_window_blockage_and_oldest_counterexample(self):
        p = Program(4,((2,3),))
        opt = solve(p,3,2,True)
        self.assertEqual(opt["cycles"],2)
        self.assertTrue(check_certificate(opt)["valid"])
        self.assertEqual(replay(4,p.edges,3,2,greedy(p,3,2)),3)
        self.assertEqual(greedy(p,3,2),[[0,1],[2],[3]])

    def test_completed_blocked_entries_keep_slots(self):
        # At the second cycle, completed job 1 cannot free a slot past head 0.
        with self.assertRaises(ValueError): replay(3,(),2,2,[[1],[0,2]])
        self.assertEqual(replay(3,(),2,2,[[1],[0],[2]]),3)

    def test_no_same_cycle_dependencies(self):
        with self.assertRaises(ValueError): replay(2,((0,1),),2,2,[[0,1]])

    def test_offset_edges_are_not_enough(self):
        t = [1,0,2,1]
        self.assertLess(t[0],t[2]); self.assertLess(t[1],t[3])
        self.assertEqual(required_window(t),4)
        with self.assertRaises(ValueError): replay(4,(),2,2,[[1],[0,3],[2]])

    def test_data_critical_path_greedy_can_fail(self):
        p=Program(5,((1,3),(2,4),(3,4)))
        self.assertEqual(solve(p,3,2)["cycles"],3)
        self.assertEqual(replay(5,p.edges,3,2,greedy(p,3,2,"critical")),4)

    def test_saturation_thresholds_are_not_monotone(self):
        p=Program(4,((1,3),(2,3)))
        table=[[solve(p,b,w)["cycles"] for w in range(1,5)] for b in range(1,5)]
        self.assertEqual(table,[[4,4,4,4],[4,3,3,3],[4,3,2,2],[4,2,2,2]])
        bsat=[next(b for b in range(1,5) if table[b-1][w-1]==table[3][w-1]) for w in range(1,5)]
        wsat=[next(w for w in range(1,5) if table[b-1][w-1]==table[b-1][b-1]) for b in range(1,5)]
        self.assertEqual(bsat,[1,4,3,3]); self.assertEqual(wsat,[1,2,3,2])

    def test_certificate_negative_controls(self):
        x=solve(Program(4,((2,3),)),3,2,True)
        bad=copy.deepcopy(x); bad["potential"]["0"] += 1
        with self.assertRaises(ValueError): check_certificate(bad)
        bad=copy.deepcopy(x); del bad["potential"]["1"]
        with self.assertRaises(ValueError): check_certificate(bad)
        bad=copy.deepcopy(x); bad["schedule"]=[[0,1],[2,3]]
        with self.assertRaises(ValueError): check_certificate(bad)
        bad=copy.deepcopy(x); bad["potential"]["15"]=1
        with self.assertRaises(ValueError): check_certificate(bad)


if __name__ == "__main__": unittest.main()
