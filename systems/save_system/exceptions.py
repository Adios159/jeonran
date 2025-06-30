class SaveSystemError(Exception):
    """세이브 시스템 관련 기본 예외 클래스"""
    pass

class InvalidSlotError(SaveSystemError):
    """잘못된 슬롯 번호 접근 시 발생하는 예외"""
    pass

class SaveFileError(SaveSystemError):
    """파일 저장/로드 관련 예외"""
    pass

class UserCancelError(SaveSystemError):
    """사용자가 작업을 취소했을 때 발생하는 예외"""
    pass 