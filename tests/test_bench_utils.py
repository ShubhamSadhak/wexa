from bench_utils import percentile
def test_percentile():
 assert percentile([1,2,3,4],0.5)==2.5
 assert round(percentile([1,2,3,4],0.95),2)==3.85
