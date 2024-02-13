from heihachi import json_movelist_reader


def test_get_by_move_type() -> None:
    azu_move_list = json_movelist_reader.get_movelist("azucena", "src/tests/assets")

    result = json_movelist_reader.get_by_move_type("Homing", azu_move_list)
    assert len(result) > 0

    result = json_movelist_reader.get_by_move_type("homing", azu_move_list)
    assert len(result) > 0

    result = json_movelist_reader.get_by_move_type("he", azu_move_list)
    assert len(result) > 0

    result = json_movelist_reader.get_by_move_type("screw", azu_move_list)
    assert len(result) > 0


def test_get_movelist_from_json() -> None:
    result = json_movelist_reader.get_movelist("azucena", "src/tests/assets")
    assert result[0].id == "Azucena-1"


def test_get_similar_moves() -> None:
    move_list = json_movelist_reader.get_movelist("azucena", "src/tests/assets")
    similar_moves = json_movelist_reader.get_similar_moves("fff3+4", move_list)
    assert len(similar_moves) > 0


def test_get_move() -> None:
    claudio_move_list = json_movelist_reader.get_movelist("claudio", "src/tests/assets")
    move = json_movelist_reader.get_move("stb wr1+2", claudio_move_list)
    assert move is not None
    assert move.id == "Claudio-STB.f,f,F+1+2"

    azu_move_list = json_movelist_reader.get_movelist("azucena", "src/tests/assets")
    move = json_movelist_reader.get_move("d/f+1", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-df+1"

    move = json_movelist_reader.get_move("df141", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-df+1,4,1"

    move = json_movelist_reader.get_move("fc df3", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-FC.df+3"

    move = json_movelist_reader.get_move("ff3+4", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-f,F+3+4"

    move = json_movelist_reader.get_move("LIB 2", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-LIB.2"

    move = json_movelist_reader.get_move("LIB.2", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-LIB.2"

    move = json_movelist_reader.get_move("wr3", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-f,f,F+3"

    move = json_movelist_reader.get_move("f214", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-f+2,1,4"

    move = json_movelist_reader.get_move("rage d/f+1+2", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-R.df+1+2"

    move = json_movelist_reader.get_move("R.d/f+1+2", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-R.df+1+2"

    move = json_movelist_reader.get_move("H.LIB.2,F", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-H.LIB.2,F"

    move = json_movelist_reader.get_move("Heat LIB.2,F", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-H.LIB.2,F"

    move = json_movelist_reader.get_move("Heat lib2f", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-H.LIB.2,F"

    move = json_movelist_reader.get_move("ws41", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-ws4,1"

    move = json_movelist_reader.get_move("LIB d+1+3", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-LIB.d+1+3_d+2+4"

    move = json_movelist_reader.get_move("LIB d2+4", azu_move_list)
    assert move is not None
    assert move.id == "Azucena-LIB.d+1+3_d+2+4"

    jun_move_list = json_movelist_reader.get_movelist("jun", "src/tests/assets")
    move = json_movelist_reader.get_move("12u", jun_move_list)
    assert move is not None
    assert move.id == "Jun-1,2,u_d"

    move = json_movelist_reader.get_move("12d", jun_move_list)
    assert move is not None
    assert move.id == "Jun-1,2,u_d"
