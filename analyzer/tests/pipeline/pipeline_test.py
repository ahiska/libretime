import datetime
import os
from queue import Queue

import pytest

from libretime_analyzer.pipeline import Pipeline

from ..conftest import AUDIO_FILENAME, AUDIO_IMPORT_DEST


def test_run_analysis(src_dir, dest_dir):
    queue = Queue()
    Pipeline.run_analysis(
        queue,
        os.path.join(src_dir, AUDIO_FILENAME),
        dest_dir,
        AUDIO_FILENAME,
        "file",
        "",
    )
    metadata = queue.get()

    assert metadata["track_title"] == "Test Title"
    assert metadata["artist_name"] == "Test Artist"
    assert metadata["album_title"] == "Test Album"
    assert metadata["year"] == "1999"
    assert metadata["genre"] == "Test Genre"
    assert metadata["mime"] == "audio/mp3"
    assert metadata["length_seconds"] == pytest.approx(15.0, abs=0.1)
    assert metadata["length"] == str(
        datetime.timedelta(seconds=metadata["length_seconds"])
    )
    assert os.path.exists(os.path.join(dest_dir, AUDIO_IMPORT_DEST))


@pytest.mark.parametrize(
    "params,exception",
    [
        ((Queue(), "", "", ""), TypeError),
        ((Queue(), "", "", ""), TypeError),
        ((Queue(), "", "", ""), TypeError),
        ((Queue(), "", "", ""), TypeError),
    ],
)
def test_run_analysis_wrong_params(params, exception):
    with pytest.raises(exception):
        Pipeline.run_analysis(*params)
