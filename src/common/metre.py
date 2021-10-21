import logging


def summarize_metre_detection(metre_detector, acc_data, all_songs):
    logging.info(f"Metro detector: {metre_detector()}")
    logging.info(f"All: {all_songs}")
    logging.info(f"Good metre - accuracy1: {acc_data.good_accuraccy1}")
    logging.info(f"Good metre - accuracy2: {acc_data.good_accuraccy2}")
    logging.info(f"Bad: {acc_data.bad}")
    logging.info(f"Metre accuracy1: {acc_data.good_accuraccy1/all_songs}")
    logging.info(f"Metre accuracy2: {acc_data.good_accuraccy2/all_songs}")


def check_metre_detection(
    acc_data, song, result_metre, expected_metre_numerator, denumerator
):
    if check_metre_accuracy_1(song, result_metre, expected_metre_numerator):
        acc_data.good_accuraccy1 += 1
        acc_data.good_accuraccy2 += 1
    elif check_metre_accuracy_2(
        song, result_metre, expected_metre_numerator, denumerator
    ):
        acc_data.good_accuraccy2 += 1
    else:
        register_bad_metre_detection(
            song, result_metre, expected_metre_numerator, denumerator
        )
        acc_data.bad += 1


def check_metre_accuracy_1(song, result_metre, expected_metre):
    if result_metre == expected_metre:
        logging.info(
            f"Good metre detection - acc1! {expected_metre} - {song.path}: {result_metre}"
        )
        return True
    return False


def check_metre_accuracy_2(song, result_metre, expected_metre, denumerator):
    quadruples = [2, 4, 8]
    triples = [3, 6, 12]

    if (expected_metre in quadruples and result_metre in quadruples) or (
        expected_metre in triples and result_metre in triples
    ):
        logging.info(
            f"Good metre detection - acc2! {expected_metre} - {song.path}: {result_metre}"
        )
        return True
    return False


def register_bad_metre_detection(
    song, result_metre, expected_metre_numerator, denumerator
):
    logging.info(
        f"Exptected {expected_metre_numerator}/{denumerator} but detect {result_metre} - {song.path}"
    )
    return False
