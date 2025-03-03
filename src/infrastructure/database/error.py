class DataError(Exception):
    """データ関連のエラー"""


class AlreadyCreatedError(DataError):
    """既にデータが作られている場合のエラー"""
