from metre import combFilterMetreDetector, combFilterNormalizedMetreDetector, convolveMetreDetector, \
    convolveNormalizedMetreDetector, correlateNormalizedMetreDetector
from tempo import combFilterTempoDetector, convolveTempoDetector
from tests import testCase

cases = {
    # CombFilterTempo
    testCase.TestCase(True, 5, 1, combFilterTempoDetector.CombFilterTempoDetector(),
                      combFilterMetreDetector.CombFilterMetreDetector()),

    testCase.TestCase(True, 5, 2, combFilterTempoDetector.CombFilterTempoDetector(),
                      combFilterMetreDetector.CombFilterMetreDetector()),

    testCase.TestCase(True, 5, 4, combFilterTempoDetector.CombFilterTempoDetector(),
                      combFilterMetreDetector.CombFilterMetreDetector()),

    testCase.TestCase(True, 5, 8, combFilterTempoDetector.CombFilterTempoDetector(),
                      combFilterMetreDetector.CombFilterMetreDetector()),

    testCase.TestCase(True, 5, 12, combFilterTempoDetector.CombFilterTempoDetector(),
                      combFilterMetreDetector.CombFilterMetreDetector()),

    # ConvolveTempo
    testCase.TestCase(True, 5, 4, convolveTempoDetector.ConvolveTempoDetector(),
                      combFilterMetreDetector.CombFilterMetreDetector()),

    testCase.TestCase(True, 5, 8, convolveTempoDetector.ConvolveTempoDetector(),
                      combFilterMetreDetector.CombFilterMetreDetector()),

    # CombFilterMetreNormalized
    testCase.TestCase(True, 5, 4, combFilterTempoDetector.CombFilterTempoDetector(),
                      combFilterNormalizedMetreDetector.CombFilterNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 8, combFilterTempoDetector.CombFilterTempoDetector(),
                      combFilterNormalizedMetreDetector.CombFilterNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 12, combFilterTempoDetector.CombFilterTempoDetector(),
                      combFilterNormalizedMetreDetector.CombFilterNormalizedMetreDetector()),

    # ConvolveMetre
    testCase.TestCase(True, 5, 4, combFilterTempoDetector.CombFilterTempoDetector(),
                      convolveMetreDetector.ConvolveMetreDetector()),

    testCase.TestCase(True, 5, 8, combFilterTempoDetector.CombFilterTempoDetector(),
                      convolveMetreDetector.ConvolveMetreDetector()),

    testCase.TestCase(True, 5, 12, combFilterTempoDetector.CombFilterTempoDetector(),
                      convolveMetreDetector.ConvolveMetreDetector()),

    # ConvolveMetreNormalized
    testCase.TestCase(True, 5, 4, combFilterTempoDetector.CombFilterTempoDetector(),
                      convolveNormalizedMetreDetector.ConvolveNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 8, combFilterTempoDetector.CombFilterTempoDetector(),
                      convolveNormalizedMetreDetector.ConvolveNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 12, combFilterTempoDetector.CombFilterTempoDetector(),
                      convolveNormalizedMetreDetector.ConvolveNormalizedMetreDetector()),

    # CorrelateMetreNormalized
    testCase.TestCase(True, 5, 4, combFilterTempoDetector.CombFilterTempoDetector(),
                      correlateNormalizedMetreDetector.CorrelateNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 8, combFilterTempoDetector.CombFilterTempoDetector(),
                      correlateNormalizedMetreDetector.CorrelateNormalizedMetreDetector()),

    testCase.TestCase(True, 5, 12, combFilterTempoDetector.CombFilterTempoDetector(),
                      correlateNormalizedMetreDetector.CorrelateNormalizedMetreDetector()),
}
