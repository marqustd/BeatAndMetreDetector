import logging


def check_tempo_acc2(result_tempo, expected_tempo):
    range = expected_tempo * 0.02
    return (
        expected_tempo - 2 * range <= result_tempo * 2 <= expected_tempo + 2 * range
        or expected_tempo - range <= result_tempo * 0.5 <= expected_tempo + range
    )


def check_tempo_acc1(result_tempo, expected_tempo):
    range = expected_tempo * 0.02
    return expected_tempo - range <= result_tempo <= expected_tempo + range


def check_tempo_detection(acc_data, song, result_tempo, expected_tempo):
    if check_tempo_acc1(result_tempo, expected_tempo):
        logging.info(
            f"Good tempo detection - acc1! {expected_tempo} - {song.path}: {result_tempo}"
        )
        acc_data.good_accuraccy1 += 1
        acc_data.good_accuraccy2 += 1
    elif check_tempo_acc2(result_tempo, expected_tempo):
        logging.info(
            f"Good tempo detection - acc2! {expected_tempo} - {song.path}: {result_tempo}"
        )
        acc_data.good_accuraccy2 += 1
    else:
        logging.info(
            f"Exptected {expected_tempo} but detect {result_tempo} - {song.path}"
        )
        acc_data.bad += 1


def summarize_tempo_detection(tempo_detector, acc_data, all_songs):
    logging.info(f"Tempo detector: {tempo_detector()}")
    logging.info(f"All: {all_songs}")
    logging.info(f"Good tempo - accuracy1: {acc_data.good_accuraccy1}")
    logging.info(f"Good tempo - accuracy2: {acc_data.good_accuraccy2}")
    logging.info(f"Bad: {acc_data.bad}")
    logging.info(f"Tempo accuracy1: {acc_data.good_accuraccy1/all_songs}")
    logging.info(f"Tempo accuracy2: {acc_data.good_accuraccy2/all_songs}")
