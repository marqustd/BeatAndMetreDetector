from metre import CombFilterMetreDetector, CombFilterNormalizedMetreDetector, ConvolveMetreDetector, ConvolveMetreDetector, ConvolveNormalizedMetreDetector, CorrelateNormalizedMetreDetector
from tempo import CombFilterTempoDetector, ConvolveTempoDetector
from tests import testCase

cases = {
    # # CombFilterTempo
    # testCase.TestCase(True, 5, 1, CombFilterTempoDetector.CombFilterTempoDetector(),
    #                   CombFilterMetreDetector.CombFilterMetreDetector()),
    #
    # testCase.TestCase(True, 5, 2, CombFilterTempoDetector.CombFilterTempoDetector(),
    #                   CombFilterMetreDetector.CombFilterMetreDetector()),
    #
    testCase.TestCase(True, 5, 4, CombFilterTempoDetector.CombFilterTempoDetector(),
                      CombFilterMetreDetector.CombFilterMetreDetector()),

    testCase.TestCase(True, 5, 8, CombFilterTempoDetector.CombFilterTempoDetector(),
                      CombFilterMetreDetector.CombFilterMetreDetector()),

    testCase.TestCase(True, 5, 12, CombFilterTempoDetector.CombFilterTempoDetector(),
                      CombFilterMetreDetector.CombFilterMetreDetector()),
    #
    # # ConvolveTempo
    # testCase.TestCase(True, 5, 4, ConvolveTempoDetector.ConvolveTempoDetector(),
    #                   CombFilterMetreDetector.CombFilterMetreDetector()),
    #
    # testCase.TestCase(True, 5, 8, ConvolveTempoDetector.ConvolveTempoDetector(),
    #                   CombFilterMetreDetector.CombFilterMetreDetector()),

    # CombFilterMetreNormalized
    testCase.TestCase(True, 5, 4, CombFilterTempoDetector.CombFilterTempoDetector(),
                      CombFilterNormalizedMetreDetector.CombFilterNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 8, CombFilterTempoDetector.CombFilterTempoDetector(),
                      CombFilterNormalizedMetreDetector.CombFilterNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 12, CombFilterTempoDetector.CombFilterTempoDetector(),
                      CombFilterNormalizedMetreDetector.CombFilterNormalizedMetreDetector()),

    # ConvolveMetre
    testCase.TestCase(True, 5, 4, CombFilterTempoDetector.CombFilterTempoDetector(),
                      ConvolveMetreDetector.ConvolveMetreDetector()),

    testCase.TestCase(True, 5, 8, CombFilterTempoDetector.CombFilterTempoDetector(),
                      ConvolveMetreDetector.ConvolveMetreDetector()),

    testCase.TestCase(True, 5, 12, CombFilterTempoDetector.CombFilterTempoDetector(),
                      ConvolveMetreDetector.ConvolveMetreDetector()),

    # ConvolveMetreNormalized
    testCase.TestCase(True, 5, 4, CombFilterTempoDetector.CombFilterTempoDetector(),
                      ConvolveNormalizedMetreDetector.ConvolveNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 8, CombFilterTempoDetector.CombFilterTempoDetector(),
                      ConvolveNormalizedMetreDetector.ConvolveNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 12, CombFilterTempoDetector.CombFilterTempoDetector(),
                      ConvolveNormalizedMetreDetector.ConvolveNormalizedMetreDetector()),

    # CorrelateMetreNormalized
    testCase.TestCase(True, 5, 4, CombFilterTempoDetector.CombFilterTempoDetector(),
                      CorrelateNormalizedMetreDetector.CorrelateNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 8, CombFilterTempoDetector.CombFilterTempoDetector(),
                      CorrelateNormalizedMetreDetector.CorrelateNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 12, CombFilterTempoDetector.CombFilterTempoDetector(),
                      CorrelateNormalizedMetreDetector.CorrelateNormalizedMetreDetector()),

    # # best
    # testCase.TestCase(True, 3, 12, CombFilterTempoDetector.CombFilterTempoDetector(),
    #                   CorrelateNormalizedMetreDetector.CorrelateNormalizedMetreDetector()),
    # testCase.TestCase(True, 3, 16, CombFilterTempoDetector.CombFilterTempoDetector(),
    #                   CorrelateNormalizedMetreDetector.CorrelateNormalizedMetreDetector()),
}
